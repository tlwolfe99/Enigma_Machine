<?php
// =================================================================
// Display file text
// =================================================================
// 
// -----------------------------------------------------------------
//
// History:
//
//   11/30/2014 - TL Wolfe - original code completed 
//
// =================================================================

// -----------------------------------------------------------------
// file name?
// -----------------------------------------------------------------

$file = '';

if (isset($_REQUEST['file']))
{
   $file =  $_REQUEST['file'];
}
else
{
   echo "<h2>Error - no file specified in request<h2>\n";
   exit();
}

if (!file_exists($file))
{
  echo "<h2>Error - file (" . $file . ") not found<h2>\n";
  exit();  
}

// -----------------------------------------------------------------
// start webpage
// -----------------------------------------------------------------

$name = basename($file);

echo "<h1>" . $name . "</h1>\n";

// -----------------------------------------------------------------
// display file text
//
// Note:
//   str_replace is used to replace '<' with &amp;lt; and '>'
//   with &amp;gt; in the text so they will not be interperted as
//   HTML by the browser. This is a problem when displaying this
//   file (php code) in a web page. For example, '<','<' should
//   be displayed as '<','& lt;' (no space) in the str_replace
//   call. The code must be fixed if you copy it and use it.
//
//   (There does not seem to be a way of escaping this chicken
//   and egg problem. I want the str_replace call to not be
//   effected, but everything else to be fixed.) 
// -----------------------------------------------------------------

$fh = fopen($file,"r");
$txt = fread($fh,filesize($file));
fclose($fh);
$txt = str_replace('&','&amp;',$txt);
$txt = str_replace('<','&lt;',str_replace('>','&gt;',$txt));
echo "<div style=\"font-size:0.9em\"><pre>\n";
echo $txt;
echo "</pre></div>\n";

// -----------------------------------------------------------------
// end webpage
// -----------------------------------------------------------------

?>