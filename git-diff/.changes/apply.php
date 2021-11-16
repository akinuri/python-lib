<?php

// ini_set("display_errors", "1");
// error_reporting(E_ALL);

date_default_timezone_set("Europe/Istanbul");

$pw = "foo";

if (($_GET["pw"] ?? null) != $pw) {
    http_response_code(401);
    die("<p>HTTP 401 Unauthorized</p>");
}

if (file_exists("changes.zip")) {
    
    echo "<p>A \"changes.zip\" file is found.</p>";
    
    echo "<p>Extracting the zip file...</p>";
    
    $extractResult = shell_exec("unzip changes.zip ...");
    
    echo "UNZIP: " . $extractResult;
    
    echo "<p>Files are extracted.</p>";
    
    echo "<p>Archiving the zip file.</p>";
    
    $newName = date("Y-m-d_H-i-s") . ".zip";
    $newPath = "./archive" . DIRECTORY_SEPARATOR . $newName;
    $archived = rename("changes.zip", $newPath);
    
    if (!$archived) {
        die("<p>ERROR: Could not archive the zip file.</p>");
    }
    
    echo "<p>The zip file is archived under the name: $newName</p>";
    
    echo "<p>All done.</p>";
    
} else {
    echo "<p>No change file is found.</p>";
}