LATEX=pdflatex
OPTIONS= -synctex=1 -interaction=errorstopmode
DIR=/Users/maths/00_COURS/1415-cours-mounier
clean:
	rm -f *.log *.aux *.nav *.out *.toc *.nav *.snm *.synctex.gz
TEACH: Cours.tex
	@${LATEX} ${OPTIONS} -jobname=Cours_prof '\def\isprof{true}\input{Cours.tex}'
STUD: Cours.tex
	@${LATEX} ${OPTIONS} -jobname=Cours Cours.tex
TEACH-IE: Cours.tex
	@${LATEX} ${OPTIONS} -jobname=Interrogation_prof '\def\isprof{true}\input{Interrogation.tex}'
STUD-IE: Cours.tex
	@${LATEX} ${OPTIONS} -jobname=Interrogation Interrogation.tex
all: Cours.tex
	make TEACH
	make STUD
	make TEACH-IE
	make STUD-IE
	make clean
