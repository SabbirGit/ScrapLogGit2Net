#!/bin/bash


if [ ! "$BASH_VERSION" ] ; then
    echo "Please do not use sh to run this script ($0), just execute it directly" 1>&2
    exit 1
fi



if [ ! "$BASH_VERSION" ] ; then
    exec /bin/bash "$0" "$@"
fi


source config.cfg

echo -e "\n Figures should be in Figures folder\n"
FIGURE_TO_DEPLOY=Figures/all-known-org.pdf


echo "Testing if $FOCAL_ORG pdf figure is there"

{
if [ ! -f $FIGURE_TO_DEPLOY]; then
    echo "$FIGURE_TO_DEPLOY - File not found!"
    exit 0
fi
}


CMD="du -sh $FIGURE_TO_DEPLOY"
echo $CMD
eval $CMD
echo ""



CMD="file $FIGURE_TO_DEPLOY"
echo $CMD
eval $CMD
echo ""



echo "Cropping the margins"

CMD="pdf-crop-margins -v -p 0 -a -1 $FIGURE_TO_DEPLOY  "
echo $CMD
eval $CMD
echo ""




echo "Coping the result to the Figures folder" 

CMD="cp $FIGURE_TO_DEPLOY ./Figures/" 
echo $CMD
eval $CMD
echo ""


echo "Showing the result"




CMD="okular $FIGURE_TO_DEPLOY""_cropped.pdf"
echo $CMD
eval $CMD
echo ""



echo "Listing the destination Figures folder"

CMD="ls $OVERLEAF_FIGURES_FOLDERS" 
echo $CMD
eval $CMD
echo ""




# Copying the figure pdf file
CMD="cp -iv $FIGURE_TO_DEPLOY""_cropped.pdf $OVERLEAF_FIGURES_FOLDERS" 
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


CMD="git commit $FIGURE_TO_DEPLOY""_cropped.pdf -m '4-deploy-to-overlead.sh added pdfFigure for $FOCAL_ORG'"
echo $CMD
eval $CMD
echo ""

CMD="git push"
echo $CMD
eval $CMD
echo ""



echo "back to origin" 
cd - 

echo "DONE"


