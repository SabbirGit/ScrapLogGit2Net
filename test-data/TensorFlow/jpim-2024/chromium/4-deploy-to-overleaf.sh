#!/bin/bash

source config.cfg


echo "Testing if $FOCAL_ORG pdf figure is there"

CMD="du -sh $FOCAL_ORG.pdf"
echo $CMD
eval $CMD
echo ""



CMD="file $FOCAL_ORG.pdf"
echo $CMD
eval $CMD
echo ""



echo "Cropping the margins"
 input.pdf

CMD="pdf-crop-margins -v -p 0 -a -1 $FOCAL_ORG.pdf"
echo $CMD
eval $CMD
echo ""


echo "Showing the result"

CMD="okular $FOCAL_ORG""_cropped.pdf"
echo $CMD
eval $CMD
echo ""



echo "Listing the destination Figures folder"

CMD="ls $OVERLEAF_FIGURES_FOLDERS" 
echo $CMD
eval $CMD
echo ""



# Copying the figure pdf file
CMD="cp -iv $FOCAL_ORG""_cropped.pdf $OVERLEAF_FIGURES_FOLDERS" 
echo $CMD
eval $CMD
echo ""


echo "Adding to version control"
cd $OVERLEAF_FIGURES_FOLDERS

echo $PWD
echo "I moved to $PWD"
echo ""

CMD="git add $FOCAL_ORG""_cropped.pdf"
echo $CMD
eval $CMD
echo ""


CMD="git commit $FOCAL_ORG""_cropped.pdf -m '4-deploy-to-overlead.sh added pdfFigure for $FOCAL_ORG'"
echo $CMD
eval $CMD
echo ""

CMD="git push"
echo $CMD
eval $CMD
echo ""

echo "Now check than main exists" 

MAIN_FILE=main.tex

# Check if the file is provided
if [ -f OVERLEAF_FIGURES_FOLDERS/$MAIN_FILE ]; then
    echo "main.tex missing"
    exit 1
fi

echo "File is provided"

# LaTeX code to be inserted
FIGURE_CODE="\n\\begin{figure}[h!]\n\\centering\n\\includegraphics[width=0.8\\textwidth]{test.pdf}\n\\caption{Description of the figure}\n\\label{fig:test}\n\\end{figure}\n"

echo "FIGURE_CODE=$FIGURE_CODE"

# Use sed to insert the figure code after the specified line
sed -i "/\\subsection{BOT added figures}/a $FIGURE_CODE" "$MAIN_FILE"



# Use sed to insert the figure code after the specified line
#CMD="sed -i /\\subsection{BOT added figures}/a $FIGURE_CODE $MAIN_FILE" 

echo $CMD
eval $CMD
echo ""


echo "Figure code inserted into $MAIM_FILE"


echo "Testing if there with grep "

CMD="grep fig:$FOCAL_ORG $MAIN_FILE" 

echo $CMD
eval $CMD
echo ""


echo "back to origin" 
cd - 







