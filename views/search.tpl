#include "views/common_header.tpl"

<div class="well">

<h1>Select a search:</h1>
<br />

<input type="radio" rel="bin" name="mselector" value="bin" id="bincb" onclick="mostrarsolo1('searchbin');" /><a href="#" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Delimited chromosome fraction on the genetic map of the S. pennellii introgression lines population');return false" onclick="mostrarsolo1('searchbin');document.getElementById('bincb').checked = 'true';">Bin</a>

    <br />
<input type="radio" rel="mirna" name="mselector" value="mirna" id="mirnacb" onclick="mostrarsolo1('searchmicro');" /><a href="#" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Name of the plant microRNA');return false" onclick="mostrarsolo1('searchmicro');document.getElementById('mirnacb').checked = 'true';">miRNA</a>
    <br />  
<input type="radio" rel="target" name="mselector" value="target" id="targetcb" onclick="mostrarsolo1('searchtarget');" /><a href="#" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Putative target name; could be a Bacterial Artificial Chromosome (BAC) anchored to the tomato genome or an Unigene (<a href=\'http://www.sgn.cornell.edu\'>SGN</a>)');return false" onclick="mostrarsolo1('searchtarget');document.getElementById('targetcb').checked = 'true';">Target</a>
    <br />
<input type="radio" rel="keyword" name="mselector" value="keyword" id="keywordcb" onclick="mostrarsolo1('searchkey');" /><a href="#" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Search by keyword in fields: QTL and/or Metabolites and/or Hit Definition.');return false" onclick="mostrarsolo1('searchkey');document.getElementById('keywordcb').checked = 'true';">Keyword</a>

<div ID="searchbin">
<h2>Search by Bin</h2> 
<p class="note">Select a bin from the drop-down menu.</p> 
<form action="binResult" method="post"> 
  Bin Number : <select name="bin">
#include "views/binlist.tpl"
</select> <br /> 
#include "views/displayopts.tpl"

<div ID="searchmicro">
<h2>Search by Micro</h2> 
<p class="note">Select a micro from the drop-down menu.</p> 
<form action="microResult" method="post"> 
  Micro code: <select name="micro_val">
#include "views/microlist.tpl"
</select> <br /> 
#include "views/displayopts.tpl"

<div ID="searchtarget">
<h2>Search by Target</h2> 
<p class="note">Enter a target name like "SGN-U566117", "C02SLe0022J22.1" (without  quotes).</p> 
<form action="targetResult" method="post">

<label for="myInput">Target name:</label> 
<div id="myAutoComplete"> 
	<input name="target_val" id="myInput" type="text"> 
	<div id="myContainer"></div> 
</div> 
<script type="text/javascript" src="/${STATIC_URL}/js/data3.js"></script> 

 <br />
#include "views/displayopts.tpl"

<div ID="searchkey">
<h2>Search by Keyword</h2> 
<p class="note">Enter a keyword like "copper", "resistance" (without  quotes).</p> 
  <form action="keywordResult" method="post"> 
  Keyword to search : <input name="searchkey" type="text" value="" size=30 /> 
<br/>
Fields to search:<br /> 
  <input name="qtl_s" type="checkbox" checked /> 
    QTL <input name="meta_s" type="checkbox" checked /> Metabolites <input name="hitdef_s" type="checkbox" checked /> 
    Hit Definition<br /> 
<br /> 
#include "views/displayoptsnoxml.tpl"

</div>
#include "views/common_footer.tpl"

