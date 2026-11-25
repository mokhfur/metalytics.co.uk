<?php
/**
 * Metalytics — enquiry form handler.
 *
 * Serves all three forms (Request a meeting / Request a Review / Request a Demo).
 * Responds with JSON when the page submits by fetch(), and falls back to a
 * redirect for browsers without JavaScript.
 *
 * ---------------------------------------------------------------------------
 * SETTINGS — change MAIL_TO to the inbox that should receive enquiries.
 * MAIL_FROM must stay on this site's own domain or Hostinger will not send it.
 * ---------------------------------------------------------------------------
 */
const MAIL_TO   = 'info@metalytics.co.uk';
const MAIL_FROM = 'no-reply@metalytics.co.uk';
const SITE_NAME = 'Metalytics';

const FORM_LABELS = [
    'meeting' => 'Request a meeting',
    'review'  => 'Request a Review',
    'demo'    => 'Request a Demo',
];

/* ------------------------------------------------------------------ utils */

function wants_json(): bool {
    $accept = $_SERVER['HTTP_ACCEPT'] ?? '';
    return str_contains($accept, 'application/json');
}

function respond(bool $ok, string $error = "", string $redirect = "/thank-you") {
    if (wants_json()) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } elseif ($ok) {
        header('Location: ' . $redirect, true, 303);
    } else {
        header('Location: /?error=' . rawurlencode($error), true, 303);
    }
    exit;
}

/** Collapse whitespace and strip anything that could forge a mail header. */
function clean(string $key, int $max = 200): string {
    $v = (string)($_POST[$key] ?? '');
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);
    $v = trim(preg_replace('/\s+/u', ' ', $v));
    return mb_substr($v, 0, $max);
}

/* ------------------------------------------------------------- validation */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'Method not allowed.');
}

// Honeypot: real people never fill this in.
if (clean('website') !== '') {
    respond(true);   // silently accept, send nothing
}

$first   = clean('first_name', 80);
$last    = clean('last_name', 80);
$email   = clean('email', 190);
$company = clean('company', 120);
$role    = clean('position', 120);

$message = (string)($_POST['message'] ?? '');
$message = trim(preg_replace('/[^\P{C}\n]+/u', '', $message));
$message = mb_substr($message, 0, 4000);

$formKey = clean('form_name', 40);
$formLabel = FORM_LABELS[$formKey] ?? 'Website enquiry';

if ($first === '' || $last === '') {
    respond(false, 'Please give your first and last name.');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please give a valid email address.');
}

/* ------------------------------------------------------------------- send */

$name = $first . ' ' . $last;

$lines = [
    'Form:     ' . $formLabel,
    'Name:     ' . $name,
    'Email:    ' . $email,
    'Company:  ' . ($company !== '' ? $company : '—'),
    'Position: ' . ($role !== '' ? $role : '—'),
    '',
    'Message:',
    $message !== '' ? $message : '(no message)',
    '',
    str_repeat('-', 56),
    'Sent from ' . SITE_NAME . ' on ' . gmdate('d M Y H:i') . ' UTC',
    'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
];

$subject = sprintf('[%s] %s — %s', SITE_NAME, $formLabel, $name);

$headers = [
    'From: ' . sprintf('%s <%s>', SITE_NAME, MAIL_FROM),
    'Reply-To: ' . sprintf('%s <%s>', $name, $email),
    'Content-Type: text/plain; charset=UTF-8',
    'MIME-Version: 1.0',
    'X-Mailer: PHP/' . phpversion(),
];

$sent = @mail(
    MAIL_TO,
    '=?UTF-8?B?' . base64_encode($subject) . '?=',
    implode("\n", $lines),
    implode("\r\n", $headers),
    '-f' . MAIL_FROM
);

if (!$sent) {
    error_log('[metalytics] mail() failed for ' . $email);
    respond(false, 'We could not send your message just now. Please email us directly.');
}

respond(true);
