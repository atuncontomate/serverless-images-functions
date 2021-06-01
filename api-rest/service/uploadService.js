const { BlobServiceClient, StorageSharedKeyCredential } = require("@azure/storage-blob");

const account = process.env.ACCOUNT_NAME || 'account';
const accountKey = process.env.ACCOUNT_KEY || 'accountKey';
const containerName = process.env.CONTAINER_NAME || 'containerName';

async function uploadImageToResize(image) {
    
    const sharedKeyCredential = new StorageSharedKeyCredential(account, accountKey);
    const blobServiceClient = new BlobServiceClient(`https://${account}.blob.core.windows.net`, sharedKeyCredential);

    const { buffer, mimetype } = image;
    let { originalname } = image;
    originalname = "input/"+originalname;
    const containerClient = blobServiceClient.getContainerClient(containerName);

    const blobOptions = {
        blobHTTPHeaders: {
            blobContentType: mimetype
        }
    };

    const blockBlobClient = containerClient.getBlockBlobClient(originalname);
    await blockBlobClient.upload(buffer, Buffer.byteLength(buffer), blobOptions);

    return `${containerName}/${originalname}`
}

exports.uploadImageToResize = uploadImageToResize;