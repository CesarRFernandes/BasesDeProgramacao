<html>
    <head>
        <title>Multiplo de 5 entre 1 a 100</title>
    </head>
    <body>
        <?php
        for ($i = 1; $i < 101; $i++)
        {
            $mult = $i % 5;
            if($mult == 0){
                echo "$mult.'<br>'";
            }
        }
        ?>
    </body>
</html>