<?php
/**
 * Created by IntelliJ IDEA.
 * User: jencek
 * Date: 10.2.20
 * Time: 16:52
 */

class Sensor {
    public $title;
    public $info;
    public $coordinates;
    public $measured;
    public $min_distance_error;
    public $avg_distance_error;
    public $max_distance_error;
    public $times;
}

function getValues($name, $values, $encapsulate) {
    return "\"".$name."\": [".implode(",", $values)."]\n";
}

function getSensor($id, $level, $end, $sensor) {

    $SQL = "SELECT 
            min(distance_error) min_de,
            avg(distance_error) avg_de, 
            max(distance_error) max_de,
            avg(measure) me, 
            DATE_FORMAT(min(sensed), '%Y-%m-%d') se 
            FROM sensor_id".$id." 
            WHERE sensed BETWEEN adddate(STR_TO_DATE('".$end."','%Y-%m-%d'), -7) and STR_TO_DATE('".$end."','%Y-%m-%d') 
            GROUP BY DATE_FORMAT(sensed, '%Y%m%d')";

//    echo $SQL;
//    die();

    $rec = mysqli_query($GLOBALS["___mysqli_ston"], $SQL);

    $min_de = [];
    $avg_de = [];
    $max_de = [];
    $me = [];
    $se = [];
    while ($row = mysqli_fetch_array($rec,MYSQLI_ASSOC)){
        array_push($min_de, floatval($row["min_de"]));
        array_push($avg_de, floatval($row["avg_de"]));
        array_push($max_de, floatval($row["max_de"]));
        array_push($me, floatval($row["me"]));
        array_push($se, $row["se"]);
    }

    $sensor->measured = $me;
    $sensor->min_distance_error = $min_de;
    $sensor->avg_distance_error = $avg_de;
    $sensor->max_distance_error = $max_de;
    $sensor->times = $se;

    echo json_encode(get_object_vars($sensor));

}

require_once('config.php');
$con = connect();

mysqli_query($GLOBALS["___mysqli_ston"], "set names utf8") or die("Some error occurs. Please try again. Use button Back in your browser.");

$s1 = new Sensor();
$s1->title = "X1";
$s1->info = "IX1";
$s1->coordinates = [18, 50];

$s2 = new Sensor();
$s2->title = "X2";
$s2->info = "IX2";
$s2->coordinates = [18.2, 49.8];

$end = "2020-01-25";
if (isset($_REQUEST["end"])) {
    $end = $_REQUEST["end"];
}

echo "{
  \"sensors\": [";
getSensor(1, "d", $end, $s1);
echo ", ";
getSensor(2, "d", $end, $s2);
echo "]}";

((is_null($___mysqli_res = mysqli_close($con))) ? false : $___mysqli_res);

?>
