<?php
        session_start();
        print_r($_SESSION);
        $_SESSION["favcolor"] = "green";
        $servername = "212.1.210.79";
        $username = "nishantj_dbuser";
        $password = "admin";
        $dbname = "nishantj_MH05EJ4657";
        $GLOBALS["sql"]="SELECT * FROM tabind";
        // Create connection
        $GLOBALS["conn"] = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($GLOBALS["conn"]->connect_error) {
          die("Connection failed: " . $GLOBALS["conn"]->connect_error);
        }
        function display($sql){
          $count=0;
          $newrow=true;
          $result = $GLOBALS["conn"]->query($sql);

          if ($result->num_rows > 0) {
              // output data of each row
              while($row = $result->fetch_assoc()) {
                if($newrow){
                    echo "<div class='row'>";
                    $newrow=false;
                }
              echo "<div class='col' style='background-color: aqua'>";
              echo "<div class='card mx-auto' style='width: 18rem'>";
              echo "<img src='/img/indoor/{$row['imgname']}' class='card-img-top' alt='...' />";
              echo "<div class='card-body'>";
              echo "<h5 class='card-title'>Card title</h5>";
              echo "<p class='card-text'>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.</p>";
              echo "<a href='#' class='btn btn-primary'>Go somewhere</a>";
              echo "</div>";
              echo "</div>";
              echo "</div>";

              $count++;
              if($count==4){
                echo "</div>"
                $newrow=true;
                $count=0;
              }
              }
          }
        
      }
       
      if(isset($_POST['indbut'])){
        display($GLOBALS["sql"])
      }
      $conn->close();
?>
<?php
     function display($sql,$conn){
        $count=0;
        $newrow=true;
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
              if($newrow){
                  echo "<div class='row'>";
                  $newrow=false;
              }
             echo "<div class='col' style='background-color: aqua'>";
             echo "<div class='card mx-auto' style='width: 18rem'>";
             echo "<img src='/img/indoor/{$row['imgname']}' class='card-img-top' alt='...' />";
             echo "<div class='card-body'>";
             echo "<h5 class='card-title'>Card title</h5>";
             echo "<p class='card-text'>
                Some quick example text to build on the card title and make up
                the bulk of the card's content.</p>";
             echo "<a href='#' class='btn btn-primary'>Go somewhere</a>";
             echo "</div>";
             echo "</div>";
             echo "</div>";

             $count++;
             if($count==4){
               echo "</div>"
               $newrow=true;
               $count=0;
             }
            }
        }
        
      }
       
?>