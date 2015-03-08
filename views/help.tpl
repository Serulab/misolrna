#encoding UTF-8 
#include "views/common_header.tpl"

<div class="well">

            <h2>Help</h2>            



<p>
The "search tab" allows to explore the database using different queries: <strong>BIN</strong> 
(e.g. “1A” following the tomato genome dissection proposed by Eshed and Zamir, 
Euphytica 79: 175-179, 1994), <strong>miRNA name</strong> (e.g. “ath-MIR1456a” as 
proposed at the miRBASE <a href="http://www.mirbase.org">www.mirbase.org</a> ), 
<strong>Target</strong> gene (UNIGENE e.g. “SGN-U562666” or BAC e.g. “C00HBa0008K08.1” following the 
SGN nomenclature) or <strong>Keyword/s</strong> which will search using all alpha-numerical fields within the 
three selectable database fields: <strong>QTL</strong> names (metabolic and yield associated 
traits as defined by Schauer et al, Nature Biotechnology 24: 447-454, 2006), <strong>Metabolites</strong> 
names or <strong>Hit Definition</strong> that indicates target genes associated 
function ( e.g. a keyword like "copper", "glucose", "resistance" -without quotes- respectively).
</p><p>
Bottom panel allows choosing how (and which) results will be displayed; QTL, 
target map position onto the Tomato EXPEN2000 genetic map (<a href="http://solgenomics.net">solgenomics.net</a>), 
hit definition (gene annotation), alignment (between the mature miRNA and 
the predicted target) and target expression profile along tomato fruit development 
and ripening (Carrari et al, Plant Physiology 142:1380-1396, 2006).
</p><p>
BLAST tab allows searching the miSolRNA database by query sequences of user 
interest of precursors and mature miRNAs, or target genes (UNIGENES and/or BACs). 
The search may take a couple of minutes. Results can be retrieved in table formats.
</p><p>
Result pages display links to target UNIGENES, genomic clones (BAC and/or COS) 
and related publications to miRNAs.
</p>





</div>
#include "views/common_footer.tpl"

