#include "views/common_header.tpl"


<div class="well">

<h2>Welcome to miSolRNA</h2>

<p>Tomato offers one of the best model systems for fleshy fruit development and ripening studies. 
A vast source of genomic information together with fruit metabolism studies has been recently released and allows us to build a relational database. 
The database is normalized and groups 6 tables holding information about <a href="http://www.sgn.cornell.edu/">map position</a> of predicted <a href="http://asrp.cgrb.oregonstate.edu/">miRNA</a> target genes, their <a href="http://www.ncbi.nlm.nih.gov/pubmed/17071647?ordinalpos=5&itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_RVDocSum">expression patterns</a> and co-localization with <a href="http://www.ncbi.nlm.nih.gov/pubmed/16531992?ordinalpos=15&itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_RVDocSum">previously identified fruit metabolic QTLs</a>. 
Relations within the whole data set were established by means of the following fields: miRNA name, target name, target position and genetic BINs.</p>

<p>miRNA data is collected from peer-reviewed published articles. 
Data extraction and conversion was done using Python scripts. 
The database is accessible via a web interface that contains several features such as a simple search by genetic BIN, miRNA, Name, keywords, browsing, bulk data downloading and help. 
The database is licensed under General Public License (GPL). Currently there are over 57 entries for miRNAs.</p>

<p>The fast growing set of genomic data along side with newly discovered sRNAs and miRNAs found in different plant species will allow us periodically update this DB with new relations; we provide a RSS feed to keep updated all interested users. 
We will also very much appreciate your feedback comments and suggestions.</p>

</div>


#include 'views/common_footer.tpl'