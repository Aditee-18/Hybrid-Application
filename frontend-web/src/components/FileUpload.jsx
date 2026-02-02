import {useState} from 'react';
import {uploadCSV} from '../services/api';

const FileUpload=({onUploadSuccess}) =>{
    const [file,setFile]=useState(null);
    const [loading,setLoading]=useState(false);

    const handleFileChange=(e)=>{
        setFile(e.target.files[0]);
    };

    const handleUpload=async()=>{
        if(!file) return alert("Please select a file first!");

        setLoading(true);
        try{
            const data=await uploadCSV(file);
            onUploadSuccess(data);
        }catch(err){
            alert("Failed to upload file");
        }finally{
            setLoading(false);
        }
    };

    return(
        <div className='upload-section'>
            <input type="file" accept=".csv" onChange={handleFileChange}/>
            <button onClick={handleUpload} disabled={loading}>
                {loading? "Processing": "Analyze Equipment Data"}
            </button>

        </div>
    );


};

export default FileUpload;
