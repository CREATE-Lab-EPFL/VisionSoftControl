"""Graphviz diagrams: network map for Fig. 3 (labels + tensor sizes as in the
code) and the proposed Fig. 4c signal-flow revision."""
import subprocess

OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision/figures"

net = r'''digraph G {
rankdir=LR; nodesep=0.18; ranksep=0.4; newrank=true;
node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, penwidth=0.8, margin="0.08,0.04"];
edge [fontname="Helvetica", fontsize=9, arrowsize=0.6];
subgraph cluster_s { label=<<B>Single section</B>>; fontname="Helvetica"; fontsize=11; style=dashed; color="#999999";
 img1 [label=<Image<BR/>1 x 480 x 640>, fillcolor="#eeeeee"];
 bb1 [label=<MobileNetV2 features<BR/>(new 1-ch first conv)<BR/>GAP: 1280>, fillcolor="#dbe9f6"];
 fp1 [label=<<B>f<SUB>p</SUB><SUP>1</SUP></B> head<BR/>Linear 1280 to 6>, fillcolor="#cfe8cf"];
 fc1 [label=<<B>f<SUB>C</SUB><SUP>1</SUP></B> heads<BR/>Linear 1280 to 5|4|3>, fillcolor="#f6dccf"];
 p1 [label=<tip pose (6)>, shape=ellipse, fillcolor="#cfe8cf"];
 c1 [label=<curvature (5|4|3)<BR/>L, c<SUB>0</SUB>..c<SUB>2</SUB>, phi>, shape=ellipse, fillcolor="#f6dccf"];
 img1 -> bb1; bb1 -> fp1 -> p1; bb1 -> fc1 -> c1;
 nl1 [label=<<B>N<SUB>l</SUB><SUP>1</SUP></B> (IK)<BR/>tip position (3) to tendons (3)<BR/>residual MLP, 128, BN, LeakyReLU>, fillcolor="#e6dcf2"];
 nc [label=<<B>N<SUB>C</SUB></B> (labels only, offline)<BR/>section-tip pose (6) to curvature (5|4|3)<BR/>residual MLP, 128>, fillcolor="#f6dccf"];
}
subgraph cluster_m { label=<<B>Three sections</B>>; fontname="Helvetica"; fontsize=11; style=dashed; color="#999999";
 img3 [label=<Images<BR/>3 x 480 x 640<BR/>(1 camera per channel)>, fillcolor="#eeeeee"];
 bb3 [label=<MobileNetV2 features<BR/>(pretrained 3-ch first conv)<BR/>GAP: 1280>, fillcolor="#dbe9f6"];
 fp3 [label=<<B>f<SUB>p</SUB><SUP>3</SUP></B> head<BR/>1280 to 512 to 18>, fillcolor="#cfe8cf"];
 fc3 [label=<<B>f<SUB>C</SUB><SUP>3</SUP></B> heads<BR/>1280 to 512 to 15|12|9>, fillcolor="#f6dccf"];
 p3 [label=<3 section-tip poses (18)>, shape=ellipse, fillcolor="#cfe8cf"];
 c3 [label=<curvature, 3 sections<BR/>(15|12|9)>, shape=ellipse, fillcolor="#f6dccf"];
 img3 -> bb3; bb3 -> fp3 -> p3; bb3 -> fc3 -> c3;
 np3 [label=<<B>N<SUB>p</SUB><SUP>3</SUP></B> (FK)<BR/>tendons (9) to tip-III pose (6)<BR/>MLP 4 x 128, ELU>, fillcolor="#fff2cc"];
 nl3 [label=<<B>N<SUB>l</SUB><SUP>3</SUP></B> (IK)<BR/>tip-III pose (6) to tendons (9)<BR/>MLP 4 x 128, ELU>, fillcolor="#e6dcf2"];
 np3 -> nl3 [label="frozen, inside\nIK training loss", style=dashed];
}
bb1 -> bb3 [style=dashed, label="weights\ntransferred", color="#666666", constraint=false];
nc -> c3 [style=dashed, label="labels for f_C^3", color="#b05a2a", fontcolor="#b05a2a", constraint=false];
{rank=same; img1; nl1;} {rank=same; img3; np3;}
}'''

ctrl = r'''digraph G {
rankdir=LR; nodesep=0.35; ranksep=0.35;
node [shape=box, style="rounded,filled", fillcolor="#f5f5f5", fontname="Helvetica", fontsize=11, penwidth=0.8];
edge [fontname="Helvetica", fontsize=9, arrowsize=0.6];
plan [label=<Linear + SLERP<BR/>planner>]; sum [label="+ / -", shape=circle, width=0.45, fixedsize=true, fontsize=9];
ik [label=<<B>Inverse kinematics</B><BR/>model-based: J<SUP>#</SUP>(l) e + N(l) (l&#772; - l)<BR/>data-driven: (dN<SUB>l</SUB>/dp) e>, fillcolor="#e6dcf2"];
int [label=<integrate<BR/>(motor commands)>]; rob [label=<Robot>];
cam [label=<Cameras>]; pose [label=<<B>f<SUB>p</SUB></B> (pose CNN)>, fillcolor="#cfe8cf"];
enc [label=<Motor encoders>, fillcolor="#fff2cc"];
curv [label=<<B>f<SUB>C</SUB></B> (curvature CNN)<BR/>reconstruction output,<BR/>not used by the controllers>, fillcolor="#f6dccf", style="rounded,filled,dashed"];
plan -> sum [label=<p<SUB>ref</SUB>>]; sum -> ik [label="e"]; ik -> int [label=<l&#775;>]; int -> rob [label="l"]; rob -> cam;
cam -> pose; pose -> sum [label="p (camera)"];
rob -> enc; enc -> ik [label=<l (model-based only)>, color="#b8860b", fontcolor="#b8860b"];
cam -> curv [style=dashed, color="#999999"];
}'''

for name, src in [("network_map", net), ("fig4c_proposed", ctrl)]:
    open(f"{OUT}/{name}.dot", "w").write(src)
    subprocess.run(["dot", "-Tpdf", f"{OUT}/{name}.dot", "-o", f"{OUT}/{name}.pdf"], check=True)
print("diagrams done")
