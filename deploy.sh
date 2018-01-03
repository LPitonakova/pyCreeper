BUILD_PATH="doc/build/html"

function deploy() {

    echo "Deploying to $DEPLOY_PATH..."
    rsync -rlv -e 'ssh -p 18765' --password-file=pass.txt --progress --delete --exclude=".DS_Store" --exclude=".*.swp" --exclude="*.cache" --exclude="cgi-bin" --exclude="error_log"\
    ${BUILD_PATH}/ $DEPLOY_PATH

}


DEPLOY_PATH=lenkaspa@uk10.siteground.eu:/home/lenkaspa/www/pycreeper
deploy


