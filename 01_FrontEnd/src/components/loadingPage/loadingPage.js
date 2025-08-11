import { ProcessContext } from "context/processContext";
import { SummaryContext } from "context/summaryContext";
import { UserContext } from "context/userContext";
import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import './loadingPage.css'



export default function LoadingPage(){

    const {processContext, setProcessContext} = useContext(ProcessContext);
    const {userContext} = useContext(UserContext);
    const {summaryContext, setSummaryContext} = useContext(SummaryContext);

    const navigate = useNavigate()

    useEffect(() => {

        setTimeout(function () {
            if (processContext != null){
                navigate('/results');
                console.log(summaryContext)
                console.log(processContext)
                }
        }, 5000)

    }, [processContext])

    return (
        <div className="loadingContainer">
            <h5 className="loadingTitle">Mohon tunggu sebentar...</h5>
            <br/>
            <div className="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
            <br/>
            <p className="loadingInstruction">Proses pencarian Anda sedang dilakukan. Proses ini dapat memakan waktu beberapa menit tergantung dengan jumlah pencarian</p>
        </div>
    )
}