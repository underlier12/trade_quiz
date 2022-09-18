import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import 'bootstrap/dist/css/bootstrap.min.css'

function Registration() {
    const { register, handleSubmit } = useForm()
    const [ apiResponse, setApiRespose ] = useState()
    
    const onSubmit = (event, data) => {
        // event.preventDefault()
        const REGISTRATION_URL = 'http://localhost:5000/registration/'
        const subject = data.target['subject'].value
        const article = data.target['article'].value
        const version = data.target['version'].value
        const content = data.target['content'].value

        fetch(REGISTRATION_URL+subject, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                article: article,
                version: version,
                content: content
            })
        })
            .then(res => res.json())
            .then(result => {
                // console.log(typeof(result))
                setApiRespose(result)
            })
            .catch(error => {
                console.log(error)
            })

        data.target['article'].value = ''
        // data.target['version'].value = ''
        data.target['content'].value = ''
    }

    return (
        <div>
            <div className='card'>
                <h4 className='card-header'>Registration form</h4>
                <div className='card-body'>
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Subject</label>
                            <select className='form-control' {...register('subject')}>
                                <option value="trade-english">Trade english</option>
                                <option value="international-payment">International payment</option>
                            </select>
                        </div>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Article</label>
                            <input className='form-control' {...register('article', {required: true})} />
                        </div>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Version</label>
                            {/* <input className='form-control' {...register('version', {required: true})} /> */}
                            <select className='form-control' {...register('version')}>
                                <option value="english">English</option>
                                <option value="korean">Korean</option>
                            </select>
                        </div>
                        <div className='form-group mb-1'>
                            <label className='form-label'>Content</label>
                            <input className='form-control' {...register('content', {required: true})} />
                        </div>
                        <div className='mt-4'>
                            <input className='mb-2 btn btn-primary' type="submit" />
                        </div>
                    </form>
                </div>
            </div>
            <div>
                <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
            </div>
        </div>
    )
}

export default Registration