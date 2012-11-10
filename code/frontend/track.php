<?php
header('Content-type: application/json');

$data = array(
	"id" => 1,
	"title" => "title",
	"desc" => "desc",
	"tags" => array(),
	"level" => 1
	);

header ("HTTP/1.0 200 OK");
echo json_encode($data);

?>