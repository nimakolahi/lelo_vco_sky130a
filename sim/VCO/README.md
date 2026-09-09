TB_NCM

#### Transient analysis (tran)

Check transient operation.  "Sch" is the schematic netlist,
"Lay" the post-layout netlist with extracted parasitics
(work/lpe/LELO_VCO_lpe.spi, 134 parasitic caps).



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Oscillation frequency**|**fosc** || **Spec**  | **20.0000** | **50.0000** | **120.0000** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 36.2814 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|22.9261 | 35.4883 | 53.0474 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|25.5430 | 36.7936 | 48.0443 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 31.5438 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|<span style='color:orange'>**19.7756**</span> | 30.9440 | 46.2869 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|20.8040 | 31.3089 | 41.8139 | |

