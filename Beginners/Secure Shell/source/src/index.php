<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Shell</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Courier New', Courier, monospace;
        }
        .container {
            max-width: 600px;
            padding-top: 50px;
        }
        #terminal {
            background-color: #1e1e1e;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        #output {
            background-color: #121212;
            color: #f5f5f5;
            height: 250px;
            padding: 15px;
            overflow-y: auto;
            border: 1px solid #444;
            border-radius: 8px;
            font-family: 'Courier New', Courier, monospace;
        }
        .alert-danger {
            background-color: #d9534f;
            border-color: #d9534f;
            color: white;
        }
        input[type="text"] {
            background-color: #2e2e2e;
            color: #e0e0e0;
            border: none;
            border-bottom: 2px solid #666;
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #4CAF50;
        }
        .btn-primary {
            background-color: #007bff;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 5px;
            font-size: 16px;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .header-text {
            font-size: 24px;
            font-weight: bold;
            color: #e0e0e0;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="terminal">
            <div class="header-text">Welcome to Secure Shell</div>
            <div id="output">Type a command to execute</div>
            <form id="commandForm" method="get">
                <input type="text" name="cmd" class="form-control mb-3" placeholder="Enter a safe command" autofocus>
                <input type="submit" class="btn btn-primary btn-block" value="Run Command">
            </form>
        </div>
        <div class="mt-3">
            <?php
            if (isset($_GET["cmd"])) {
                $safeCommands = ["ls", "pwd", "echo", "date"]; // Add more safe commands
                $command = $_GET["cmd"];
                $firstWord = strtok($command, " ");
                if (in_array($firstWord, $safeCommands)) {
                    echo "<pre>";
                    system($command);
                    echo "</pre>";
                } else {
                    echo "<div class='alert alert-danger'>Error: Unsafe command</div>";
                }
            }
            ?>
        </div>
    </div>

    <!-- Include Bootstrap JS (optional) -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
