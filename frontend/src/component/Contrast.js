import React, { useState } from "react";
import { useForm } from 'react-hook-form'
import 'bootstrap/dist/css/bootstrap.min.css'
import './Contrast.css'

function Contrast() {
    const { register, handleSubmit } = useForm()
    const [selectedFile, setSelectedFile] = useState();
	const [isFilePicked, setIsFilePicked] = useState(false);
    const [output, setOutput] = useState()
    const [original, setOriginal] = useState()

    const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsFilePicked(true);
        console.log(isFilePicked)
	};

    const handleSubmission = (event, data) => {
        const QUERY_URL = 'http://localhost:5000/query/'
        const DASH = '/'
		const formData = new FormData();
		formData.append('File', selectedFile);
        // formData.append('Version', data.target['version'].value)
        
        const subject = data.target['subject'].value
        const version = data.target['version'].value
        // console.log(data.target['version'].value)

        const combinedUrl = QUERY_URL+subject+DASH+version
        console.log(combinedUrl)
        
        fetch(QUERY_URL+subject+DASH+version, {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(result => {
                console.log(result)
                // var original = JSON.parse(result.original)
                const resOutput = result.output
                const resOriginal = result.original
                setOutput(resOutput)
                setOriginal(resOriginal)
            })
            .catch(error => {
                console.log(error)
            })
    }

    return (
        <div>
            <div className="card">
                <div className='card-body'>
                    <form onSubmit={handleSubmit(handleSubmission)}>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Subject</label>
                            <select className='form-control' {...register('subject')}>
                                <option value="trade-english">Trade english</option>
                                <option value="international-payment">International payment</option>
                            </select>
                        </div>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Language</label>
                            <select className='form-control' {...register('version')}>
                                <option value="eng">English</option>
                                <option value="kor">Korean</option>
                            </select>
                        </div>
                        <div className="form-group mb-1">
                            <label className='form-label'>File upload</label>
                            <input className="form-control" type='file' name='file' onChange={changeHandler}/>
                        </div>
                        <div>
                            <input className="mt-2 btn btn-primary" type="submit"/>
                        </div>
                    </form>
                </div>
            </div>
            <div className="searchResultContainer mt-3">
                <div className="left">
                    <pre className="innerLeft">{JSON.stringify(output, null, 2)}</pre>
                </div>
                <div className="right">
                    <p className="innerRight">{original}</p>
                </div>
            </div>
        </div>
    )
}

export default Contrast