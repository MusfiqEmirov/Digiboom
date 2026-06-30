<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

function respond(int $code, array $payload): void
{
    http_response_code($code);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function getArticleId(): string
{
    $raw = $_GET['id'] ?? $_POST['id'] ?? '';
    $id = preg_replace('/[^a-z0-9\-_]/i', '', (string) $raw);
    return $id ?? '';
}

function getClientIp(): string
{
    $candidates = [
        $_SERVER['HTTP_CF_CONNECTING_IP'] ?? null,
        $_SERVER['HTTP_X_FORWARDED_FOR'] ?? null,
        $_SERVER['HTTP_X_REAL_IP'] ?? null,
        $_SERVER['REMOTE_ADDR'] ?? null,
    ];

    foreach ($candidates as $value) {
        if (!$value) {
            continue;
        }
        $ip = trim(explode(',', (string) $value)[0]);
        if (filter_var($ip, FILTER_VALIDATE_IP)) {
            return $ip;
        }
    }

    return '0.0.0.0';
}

$articleId = getArticleId();
if ($articleId === '') {
    respond(400, ['error' => 'Invalid article id']);
}

$dataDir = dirname(__DIR__) . '/data/blog-views';
$dataFile = $dataDir . '/' . $articleId . '.json';

if (!is_dir($dataDir) && !mkdir($dataDir, 0755, true) && !is_dir($dataDir)) {
    respond(500, ['error' => 'Storage unavailable']);
}

$data = ['count' => 0, 'ips' => []];
if (is_file($dataFile)) {
    $decoded = json_decode((string) file_get_contents($dataFile), true);
    if (is_array($decoded)) {
        $data['count'] = (int) ($decoded['count'] ?? 0);
        $data['ips'] = is_array($decoded['ips'] ?? null) ? $decoded['ips'] : [];
    }
}

$ip = getClientIp();
$ipHash = hash('sha256', $ip . '|' . $articleId);
$alreadyViewed = in_array($ipHash, $data['ips'], true);

$method = strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET');

if ($method === 'POST' && !$alreadyViewed) {
    $data['ips'][] = $ipHash;
    $data['count'] = count($data['ips']);

    $written = file_put_contents(
        $dataFile,
        json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE),
        LOCK_EX
    );

    if ($written === false) {
        respond(500, ['error' => 'Could not save view']);
    }

    $alreadyViewed = true;
}

respond(200, [
    'id' => $articleId,
    'count' => $data['count'],
    'viewed' => $alreadyViewed,
]);
