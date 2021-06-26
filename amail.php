<?php
  use PHPMailer\PHPMailer\PHPMailer;
  use PHPMailer\PHPMailer\Exception;
  require 'PHPMailer/src/Exception.php';
  require 'PHPMailer/src/PHPMailer.php';
  require 'PHPMailer/src/SMTP.php';

  $mail = new PHPMailer();
  $mail->IsSMTP();

  $mail->SMTPDebug  = 0;  
  $mail->SMTPAuth   = TRUE;
  $mail->SMTPSecure = "tls";
  $mail->Port       = 587;
  $mail->Host       = "smtp.mail.me.com";
  $mail->Username   = "kcs.chalanthon@icloud.com";
  $mail->Password   = "vdqd-jehh-eqtg-bwle";

  $mail->IsHTML(true);
  $mail->AddAddress("kcs.chalanthon@gmail.com", "kao");
  $mail->SetFrom("kcs.chalanthon@icloud.com", "admin(apple)");
  //$mail->AddReplyTo("reply-to-email", "reply-to-name");
  //$mail->AddCC("cc-recipient-email", "cc-recipient-name");
  $mail->Subject = "Test is Test Email sent via icloudmail SMTP Server using PHP Mailer";
  $content = "<b>This is a Test Email sent via icloudmail SMTP Server using PHP mailer class.</b>";

  $mail->MsgHTML($content); 
  if(!$mail->Send()) {
    echo "Error while sending Email.";
    var_dump($mail);
  } else {
    echo "Email sent successfully";
  }
?>
