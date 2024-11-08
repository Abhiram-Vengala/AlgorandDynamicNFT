import axios from "axios";

const key = process.env.REACT_APP_PINATA_KEY||"6ea23b3b66977c9a18d4";
const secretKey = process.env.REACT_APP_PINATA_SECRET_KEY||"ec8041aabd1b3643297649fde15c70a44267379a8655c3bcb62b81572e6b37f2";

console.log(key , secretKey);
//a539cac80c8f536d9545
//7a516f61a87d6cc50698fe5905975c27c87547f97b50a5cbfe68503676a69a1c

const FormData = require("form-data");

export const uploadJSONToIpfs=async(JSONBody)=>{
    const url = `https://api.pinata.cloud/pinning/pinJSONToIPFS`;
    return axios.post(url , JSONBody,{
        headers :{
            pinata_api_key:key,
            pinata_secret_api_key:secretKey,
        }
    }).then(function(response){
        return{
            success:true,
            pinataURL: response.data.IpfsHash
        };
    }).catch(function(error){
        console.log(error)
        return{
            success:false,
            message:error.message,
        }
    });
};

export const uploadFileToIpfs=async(file)=>{
    const url = `https://api.pinata.cloud/pinning/pinFileToIPFS`;

    let data = new FormData();
    data.append('file',file);
    const metadata = JSON.stringify({
        name : 'testname',
        keyvalues:{
            exampleKey:'exampleValue'
        }
    });
    data.append('pinataMetadata',metadata);

    return axios.post(url , data , {
        maxBodyLength : 'Infinity',
        headers :{
            'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
            pinata_api_key:key,
            pinata_secret_api_key:secretKey,
        }
    }).then(function(response){
        console.log("image uploaded",response.data.IpfsHash)
        return{
            success : true,
            pinataURL : "https://gateway.pinata.cloud/ipfs/" + response.data.IpfsHash
        };
    }).catch(function(error){
        console.log(error)
        return{
            success : false,
            message :error.message,
        }
    });
};