<?php
/*
 *  CONFIGURE EVERYTHING HERE
 */

// an email address that will receive the email with the output of the form
$sendTo = "youremail@gmail.com";

// message that will be displayed when everything is OK :)
$okMessage =
    "فرم تماس با موفقیت ارسال شد. متشکرم، من به زودی با شما تماس خواهم گرفت!";

// If something goes wrong, we will display this message.
$errorMessage =
    "هنگام ارسال فرم خطایی روی داد. لطفا بعدا دوباره امتحان کنید";

/*
 *  LET'S DO THE SENDING
 */

// if you are not debugging and don't need error reporting, turn this off by error_reporting(0);
error_reporting(E_ALL & ~E_NOTICE);

try {
    if (
        count($_POST) == 0 &&
        !isset($_POST["name"]) &&
        !isset($_POST["email"]) &&
        !isset($_POST["message"])
    ) {
        throw new \Exception("فرم خالی است");
    }

    // an email address that will be in the From field of the email.
    $from = $_POST["email"];
    // The message send in email
    $message = $_POST["message"];
    // subject of the email
    $subject = $_POST["name"];

    $headers =
        "From: " .
        $from .
        "\r\n" .
        "Reply-To: " .
        $sendTo .
        "\r\n" .
        "X-Mailer: PHP/" .
        phpversion();

    // Send email
    mail($sendTo, $subject, $message, $headers);

    $responseArray = ["type" => "success", "message" => $okMessage];
} catch (\Exception $e) {
    $responseArray = ["type" => "danger", "message" => $errorMessage];
}

// if requested by AJAX request return JSON response
if (
    !empty($_SERVER["HTTP_X_REQUESTED_WITH"]) &&
    strtolower($_SERVER["HTTP_X_REQUESTED_WITH"]) == "xmlhttprequest"
) {
    $encoded = json_encode(["status" => true, "message" => $okMessage]);

    header("Content-Type: application/json");

    echo $encoded;
}
// else just display the message
else {
    $encoded = json_encode(["status" => false, "message" => $errorMessage]);

    header("Content-Type: application/json");

    echo $encoded;
}