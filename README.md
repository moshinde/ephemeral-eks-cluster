# ephemeral-eks-cluster
With the usage of lambda function to send out an email notification to delete the EKS cluster when there are no pods running

Directory structure:

eksCluster
- package
  - kubernetes module
  - eks_token module
- lambda_function.py
- ca.crt => base64 encoded certificate-authority-data
  
 create package folder with python libraries
 - pip install kubernetes --target ./package
 - pip install eks_token --target ./package
 - cd package
 - zip -r ../function.zip *
 - cd ..
 - zip -g function.zip lambda_function.py
 - zip -g function.zip ca.crt
 
 create environment variable
 - export EKS_HOST="<url>"
  
