param(
    [string]$Python = (Join-Path $PSScriptRoot '../Temp/test-python/Scripts/python.exe'),
    [string[]]$Paths = @('server', 'framework', 'module_system', 'module_infra'),
    [string]$ResourcesFile = '',
    [switch]$IncludeSmoke
)

$ErrorActionPreference = 'Stop'
$runRoot = Join-Path (Get-Location).Path ('Temp\dushan-tests\' + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$settings = @{
    TEMP = $runRoot
    TMP = $runRoot
    TMPDIR = $runRoot
    PYTHONDONTWRITEBYTECODE = '1'
    PYTHONUTF8 = '1'
    PYTHONIOENCODING = 'utf-8'
    PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    DUSHAN_DP_REPORT_DIR = $runRoot
}
if ($ResourcesFile -ne '') {
    $resourcePath = (Resolve-Path -LiteralPath $ResourcesFile).Path
    $resourceData = [System.IO.File]::ReadAllText($resourcePath) | ConvertFrom-Json
    $settings['DUSHAN_TEST_RESOURCES'] = $resourcePath
    $databaseUrl = 'mysql+aiomysql://{0}:{1}@{2}:{3}/{4}' -f `
        [Uri]::EscapeDataString($resourceData.mysql.username), `
        [Uri]::EscapeDataString($resourceData.mysql.password), `
        $resourceData.mysql.host, $resourceData.mysql.port, $resourceData.mysql.database
    $settings['DUSHAN_DATABASE_TEST_URLS'] = ConvertTo-Json -InputObject @(@{ name = 'mysql'; url = $databaseUrl }) -Compress
    $redisSettings = @{
        host = $resourceData.redis.host
        port = $resourceData.redis.port
        username = $null
        password = $resourceData.redis.password
        clients = @(@{ name = 'default'; db = 8 }, @{ name = 'second'; db = 9 })
        default_client = 'default'
    }
    $settings['DUSHAN_CACHE_TEST_REDIS'] = ConvertTo-Json -InputObject $redisSettings -Depth 4 -Compress
    $settings['DUSHAN_SECURITY_TEST_REDIS'] = $settings['DUSHAN_CACHE_TEST_REDIS']
    $settings['DUSHAN_AUTH_TEST_REDIS'] = $settings['DUSHAN_CACHE_TEST_REDIS']
    $settings['DUSHAN_SECURITY_MYSQL'] = ConvertTo-Json -InputObject @{ url = $databaseUrl } -Compress
    $settings['DUSHAN_DP_REDIS_PORT'] = [string]$resourceData.redis.port
    $settings['DUSHAN_DP_REDIS_PASSWORD'] = $resourceData.redis.password
}
$previous = @{}
try {
    foreach ($name in $settings.Keys) {
        $previous[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
        [Environment]::SetEnvironmentVariable($name, $settings[$name], 'Process')
    }
    $testPaths = @($Paths | ForEach-Object { Join-Path $PSScriptRoot $_ })
    $arguments = @('-B', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-c', (Join-Path $PSScriptRoot 'pytest.ini')) +
                 $testPaths + @('--basetemp', (Join-Path $runRoot 'fixtures'), '-o', ('cache_dir=' + (Join-Path $runRoot 'cache')),
                 '--junitxml', (Join-Path $runRoot 'results.xml'))
    if (-not $IncludeSmoke) { $arguments += @('-m', 'not smoke') }
    $ErrorActionPreference = 'Continue'
    & $Python @arguments
    $result = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    Write-Output ('JUnit report: ' + (Join-Path $runRoot 'results.xml'))
} finally {
    foreach ($name in $previous.Keys) { [Environment]::SetEnvironmentVariable($name, $previous[$name], 'Process') }
}
exit $result
