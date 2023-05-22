npm run build --prefix assets/client
aws s3 sync assets/client/build s3://${STACK_NAME,,}-website/ --exclude config.js
python -c "from stack.util import Util; print(Util.get_cdk_output('Distribution'))" | while read line ; 
do 
   aws cloudfront create-invalidation --distribution-id ${line} --paths "/*"
done
