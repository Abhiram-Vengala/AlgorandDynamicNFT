import './App.css';
import { useState } from "react";
import { uploadFileToIpfs, uploadJSONToIpfs } from './pinata';
import axios from 'axios';


function App() {
  const [fileUrl, setFileUrl] = useState(null);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [dnftResponse, setDnftResponse] = useState('');
  const [updateResponse, setUpdateResponse] = useState('');
  const [assetId, setAssetId] = useState(0);
  const [imageUrl, setImageUrl] = useState('');
  async function handleUploadFile(e) {
    var file = e.target.files[0];
    try {
      const response = await uploadFileToIpfs(file);
      if (response.success === true) {
        console.log("uploaded image to the pinata :", response.pinataURL);
      }
    } catch (e) {
      console.log("Image is Not uploaded to pinata due to :", e);
    }
  }


  async function mintNft() {
    const nftJSON = {
      name, description, image: fileUrl
    }
    try {
      const response = await uploadJSONToIpfs(nftJSON);
      if (response.success === true) {
        console.log("Uploaded JSON to pinata", response)
        setFileUrl(response.pinataURL);
        const nftdata = {
          asset_name: name,
          url: response.pinataURL
        }
    
        try {
          const response = await axios.post('http://localhost:5000/create-nft', nftdata);
          setResponseMessage(`Transaction ID:${response.data.txid} and asset ID:${response.data.asset_id}`);
          console.log(response.data.txid, response.data.asset_id);
        } catch (error) {
          setResponseMessage(`Error: ${error.response.data.error}`);
        }
      }
    } catch (e) {
      console.log("error uploading the JSON :", e);
    }
  }

  async function mintDnft() {
    const nftJSON = {
      name, description, image: fileUrl
    }
    try {
      const response = await uploadJSONToIpfs(nftJSON);
      if (response.success === true) {
        console.log("Uploaded JSON to pinata", response)
        setFileUrl(response.pinataURL);
        const dnftData = {
          asset_name: name,
          url: response.pinataURL
        }
        console.log(dnftData);
        try {
          const result = await axios.post('http://localhost:5000/create/dnft', dnftData);
          setDnftResponse(`Transaction ID:${result.data.txid} and asset ID:${result.data.asset_id}`);
          console.log(result.data.txid, result.data.asset_id);
        } catch (err) {
          setDnftResponse(`Error: ${err.result.data.error}`);
          console.error("Error response:", err.result);
        }
      }
    } catch (e) {
      console.log("error uploading the JSON :", e);
    }
  }

  async function updateDnft() {
    const dnftdata = {
      asset_id: assetId,
      url: imageUrl
    }

    try {
      const response = await axios.post('http://localhost:5000/update-dnft', dnftdata);
      setUpdateResponse(response.data.txid);
    } catch (err) {
      setUpdateResponse(`Error:${err.response.data.error}`);
    }
  }

  return (
    <div className="App">
      <div className='NFT'>
        <span>NFT Name:</span>
        <input type='text' onChange={e => setName(e.target.value)}></input>
        <div />
        <span>Description:</span>
        <input type='text' onChange={e => setDescription(e.target.value)}></input>
        <div />
        <span>upload image:</span>
        <input type='file' id='img' onChange={handleUploadFile}></input>
        <div></div>
        <button onClick={mintNft}>Mint Nft</button>
        <div />
        {responseMessage && <p>{responseMessage}</p>}
      </div>
      <div className='DNFT'>
        <button onClick={mintDnft}>Mint DNft</button>
        <div />
        {dnftResponse && <p>{dnftResponse}</p>}
        <input type='text' onChange={e => setAssetId(e.target.value)} placeholder='AssetID'></input>
        <div />
        <input type='text' onChange={e => setImageUrl(e.target.value)} placeholder='Image Url'></input>
        <div />
        <button onClick={updateDnft}>Update Dnft</button>
        {updateResponse && <p>{updateResponse}</p>}
      </div>
    </div>
  );
}

export default App;
