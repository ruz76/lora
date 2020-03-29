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

function getSensor($id, $level, $end, $sensor, $recordscount) {

    $outputformat = '%Y-%m-%d';
    $inputformat = '%Y-%m-%d';
    $addunit = 'DAY';
    $groupformat = '%Y%m%d';
    $interval = -7;
    switch ($level) {
        case "year":
            $outputformat = '%Y-%m-%d';
            $inputformat = '%Y-%m-%d';
            $addunit = 'MONTH';
            $groupformat = '%Y%m';
            $interval = -7;
            break;
        case "month":
            $outputformat = '%Y-%m-%d';
            $inputformat = '%Y-%m-%d';
            $addunit = 'DAY';
            $groupformat = '%Y%m%d';
            $interval = -7;
            break;
        case "day":
            $outputformat = '%H';
            $inputformat = '%Y-%m-%d %H:%i:%s';
            $addunit = 'HOUR';
            $groupformat = '%Y%m%d %H';
            $interval = -7;
            break;
        case "hour":
            $outputformat = '%H:%i';
            $inputformat = '%Y-%m-%d %H:%i:%s';
            $addunit = 'MINUTE';
            $groupformat = '%Y%m%d %H%i';
            $interval = -7;
            break;
        case "minute":
            $outputformat = '%H:%i%s';
            $inputformat = '%Y-%m-%d %H:%i:%s';
            $addunit = 'SECOND';
            $groupformat = '%Y%m%d %H%i%s';
            $interval = -7;
            break;
    }

    $SQL = "SELECT 
            avg(lon) lon,
            avg(lat) lat,
            min(distance_error) min_de,
            avg(distance_error) avg_de, 
            max(distance_error) max_de,
            avg(measure) me, 
            DATE_FORMAT(min(sensed), '".$outputformat."') se 
            FROM sensor_id".$id." 
            WHERE sensed BETWEEN adddate(STR_TO_DATE('".$end."','".$inputformat."'), INTERVAL ".$interval." ".$addunit.") and STR_TO_DATE('".$end."','".$inputformat."') 
            GROUP BY DATE_FORMAT(sensed, '".$groupformat."') ORDER BY se ASC";


    if ($level == "realtime") {
        $SQL = "SELECT 
            lon,
            lat,
            distance_error min_de,
            distance_error avg_de, 
            distance_error max_de,
            measure me, 
            DATE_FORMAT(sensed, '%Y-%m-%d') se 
            FROM sensor_id".$id." 
            ORDER BY sensed DESC
            LIMIT ".$recordscount;
    }


//    echo $SQL;
//    die();

    $rec = mysqli_query($GLOBALS["___mysqli_ston"], $SQL);

    $lon = [];
    $lat = [];
    $min_de = [];
    $avg_de = [];
    $max_de = [];
    $me = [];
    $se = [];
    while ($row = mysqli_fetch_array($rec,MYSQLI_ASSOC)){
        array_push($lon, floatval($row["lon"]));
        array_push($lat, floatval($row["lat"]));
        array_push($min_de, floatval($row["min_de"]));
        array_push($avg_de, floatval($row["avg_de"]));
        array_push($max_de, floatval($row["max_de"]));
        array_push($me, floatval($row["me"]));
        array_push($se, $row["se"]);
    }

    $sensor->lon = $lon;
    $sensor->lat = $lat;
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
$s1->title = "Static X1";
$s1->info = "IX1";
$s1->coordinates = [18.22554, 49.81724];

$s2 = new Sensor();
$s2->title = "Static X2";
$s2->info = "IX2";
$s2->coordinates = [18.23091, 49.82001];

$s3 = new Sensor();
$s3->title = "Dynamic X2";
$s3->info = "IX3";
$s3->coordinates = [18.23091, 49.82001];

$end = "2020-01-25";
if (isset($_REQUEST["end"])) {
    $end = $_REQUEST["end"];
}

$level = "month";
$levels = ["year", "month", "day", "hour", "minute", "realtime"];
if (isset($_REQUEST["level"]) && in_array($_REQUEST["level"], $levels)) {
    $level = $_REQUEST["level"];
}

$recordscount = 10;
$recordscounts = [1, 5, 10, 20];
if (isset($_REQUEST["recordscount"]) && in_array($_REQUEST["recordscount"], $recordscounts)) {
    $recordscount = $_REQUEST["recordscount"];
}

echo "{
  \"sensors\": [";
getSensor(1, $level, $end, $s1, $recordscount);
echo ", ";
getSensor(2, $level, $end, $s2, $recordscount);
echo ", ";
getSensor(3, $level, $end, $s3, $recordscount);
echo "]}";

((is_null($___mysqli_res = mysqli_close($con))) ? false : $___mysqli_res);

?>
