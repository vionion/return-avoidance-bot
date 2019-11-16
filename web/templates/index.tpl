<html lang="en">

<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>Document</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

<script>
    window.onload = function() {
        alert("vittun toimi")
    }
</script>

<body>
   <ul>
    % for log_event in logs.items():
        <li>{{log_event[0]}}   -    {{log_event[1]}}</li>
    % end
    </ul>

</body>

</html>