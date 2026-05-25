<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script type="text/javascript" src="script.js"></script>
</head>
<body>
    <div class="menu">
        <ul>
            <li><a href="index.php">Home</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="missStmt.html">Mission Statement</a></li>
        </ul>
    </div>
    <div>
        <h1>How busy is my area?</h1>
        <?php
        	$url = "https://api.thingspeak.com/channels/3390575/fields/1.json?results=1";
            $ch = curl_init($url);
            $headers = [
            	"Content-type: application/json;charset=utf-8",
                "Accept: text/plain"
            ];
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            $data = curl_exec($ch);
            $json = json_decode($data, 1);
            //var_dump($json);
            //var_dump($json["feeds"][0]["field1"]);
            $good = array_values($json["feeds"][0]);
            echo "<p>There are currently estimated $good[2] people in the area</p>";
            //var_dump($data);
            //$vals = array_values($json);
            //$info = substr($data, -15);
            //echo $info;
            //echo $vals;

            ?>
        <div style="text-align:center;">
            <button onclick="reload()">Refresh Page</button>
        </div>
        

    </div>
</body>
</html>