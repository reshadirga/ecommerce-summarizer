import { DownloadOutlined, PlusOutlined } from "@ant-design/icons";
import { SummaryContext } from "context/summaryContext";
import { UserContext } from "context/userContext";
import React, { useContext, useEffect, useState } from "react";
import { Button, Table } from "reactstrap";
import ProductCard from "./productCard";
import ProductCardEmpty from "./productCardEmpty";
import Parse from 'parse/dist/parse.min';
import './resultPage.css'
import { ProcessContext } from "context/processContext";
import * as XLSX from 'xlsx';
import CsvDownload from 'react-json-to-csv'
import { ExportToCsv } from 'export-to-csv';
import { Navigate, useNavigate } from "react-router-dom";

export default function ResultPage(){

    const {summaryContext, setSummaryContex} = useContext(SummaryContext);
    const {userContext, setUserContext} = useContext(UserContext);
    const {processContext, setProcessContext} = useContext(ProcessContext);
    const navigate = useNavigate()

    async function convertToCSV(array) {

        const response_clean = Object.keys(array).map(function(k) {
            return array[k];
        });

        const options = { 
            fieldSeparator: ',',
            quoteStrings: '"',
            decimalSeparator: '.',
            showLabels: true, 
            showTitle: true,
            title: 'ECM_SearchResult',
            useTextFile: false,
            useBom: true,
            useKeysAsHeaders: true,
            // headers: ['Column 1', 'Column 2', etc...] <-- Won't work with useKeysAsHeaders present!
          };
         
        const csvExporter = new ExportToCsv(options);
         
        csvExporter.generateCsv(response_clean);
      }
    
    async function downloadTable(searchId) {
        let scrapIds = await ScrapsIds(searchId)
        let jsonTable = await (await getTable(scrapIds[scrapIds.length - 1])).text()
        return JSON.parse(jsonTable)
    }

    async function ScrapsIds(searchId){
        // Your Parse initialization configuration goes here
        const PARSE_APPLICATION_ID = 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI';
        const PARSE_HOST_URL = 'https://parseapi.back4app.com/';
        const PARSE_JAVASCRIPT_KEY = 'C1PFzXvctEIjXA33a1rYy68fxdfh3bBlXzLBNEaC';
        Parse.initialize(PARSE_APPLICATION_ID, PARSE_JAVASCRIPT_KEY);
        Parse.serverURL = PARSE_HOST_URL;

        var queryIds = ""
    
        // Save user input
        try {
            // create a new Parse Object instance
            const QueryGet = new Parse.Query('ScrapResMin');
            QueryGet.contains('queryId', searchId);
            const queryResults = await QueryGet.find();
            const QueryIDs = await queryResults.map((x) => {
                queryIds = x.id + "_" + queryIds
                return queryIds
            }
            )
            console.log(queryResults)
            return QueryIDs;
        
        } catch (error) {
            console.log('Error saving to download tabel: ', error);
        }
        }

    // Connect to Python`
    async function getTable(queryId) {
        console.log(queryId);
        const res = await fetch('/download/' + queryId);
        console.log(res)
        return res;
        
    }

    async function handleClick() {
        const json_file = await downloadTable(processContext)
        convertToCSV(json_file)
    }

    function handleNewSearch() {
        setProcessContext(null)
        navigate('/')
        console.log(userContext)
    }

    return (
        <>
            <div className="searchResultHeader">
                <h5>Hasil pencarian untuk "{userContext.userInput.query}"</h5>
                <p>untuk rentang harga Rp{userContext.userInput.minPrice ? userContext.userInput.minPrice : "-"} hingga Rp{userContext.userInput.maxPrice ? userContext.userInput.maxPrice : "-"}</p>
            </div>

            <div className="resultTableContainer">
            <Table borderless hover className="resultTable">
                <thead className="resultTableHeader">
                    <tr>
                    <th>
                        {" "}
                    </th>
                    <th>
                        Blibli
                    </th>
                    <th>
                        Bukalapak
                    </th>
                    <th>
                        Shopee
                    </th>
                    <th>
                        Tokopedia
                    </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th scope="row" className="resultTableCategory">
                        Top rated
                    </th>
                    <td>{summaryContext.blibli.top ? <ProductCard product={summaryContext.blibli.top} id={"blibli5"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.bukalapak.top ? <ProductCard product={summaryContext.bukalapak.top} id={"bukalapak5"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.shopee.top ? <ProductCard product={summaryContext.shopee.top} id={"shopee5"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.tokopedia.top ? <ProductCard product={summaryContext.tokopedia.top} id={"tokopedia5"}/> : <ProductCardEmpty/> }</td>
                    </tr>
                    <tr>
                    <th scope="row"className="resultTableCategory">
                        Cheapest
                    </th>
                    <td>{summaryContext.blibli.cheap ? <ProductCard product={summaryContext.blibli.cheap} id={"blibli1"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.bukalapak.cheap ? <ProductCard product={summaryContext.bukalapak.cheap} id={"bukalapak1"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.shopee.cheap ? <ProductCard product={summaryContext.shopee.cheap} id={"shopee1"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.tokopedia.cheap ? <ProductCard product={summaryContext.tokopedia.cheap} id={"tokopedia1"}/> : <ProductCardEmpty/> }</td>
                    </tr>
                    
                    <tr>
                    <th scope="row"className="resultTableCategory">
                        Most expensive
                    </th>
                    <td>{summaryContext.blibli.expensive ? <ProductCard product={summaryContext.blibli.expensive} id={"blibli2"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.bukalapak.expensive ? <ProductCard product={summaryContext.bukalapak.expensive} id={"bukalapak2"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.shopee.expensive ? <ProductCard product={summaryContext.shopee.expensive} id={"shopee2"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.tokopedia.expensive ? <ProductCard product={summaryContext.tokopedia.expensive} id={"tokopedia2"}/> : <ProductCardEmpty/> }</td>
                    </tr>
                    
                    <tr>
                    <th scope="row"className="resultTableCategory">
                        Most sold
                    </th>
                    <td>{summaryContext.blibli.sold ? <ProductCard product={summaryContext.blibli.sold} id={"blibli3"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.bukalapak.sold ? <ProductCard product={summaryContext.bukalapak.sold} id={"bukalapak3"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.shopee.sold ?<ProductCard product={summaryContext.shopee.sold} id={"shopee3"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.tokopedia.sold ? <ProductCard product={summaryContext.tokopedia.sold} id={"tokopedia3"}/> : <ProductCardEmpty/> }</td>
                    </tr>
                    
                    {/* <tr>
                    <th scope="row"className="resultTableCategory">
                        Most reviewed
                    </th>
                    <td>{summaryContext.blibli.rating ? <ProductCard product={summaryContext.blibli.rating} id={"blibli4"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.bukalapak.rating ? <ProductCard product={summaryContext.bukalapak.rating} id={"bukalapak4"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.shopee.rating ? <ProductCard product={summaryContext.shopee.rating} id={"shopee4"}/> : <ProductCardEmpty/> }</td>
                    <td>{summaryContext.tokopedia.rating ? <ProductCard product={summaryContext.tokopedia.rating} id={"tokopedia4"}/> : <ProductCardEmpty/> }</td>
                    </tr> */}
                </tbody>
            </Table>
            
            <button className="newSearchButton btn btn-round btn-primary" onClick={(e) => handleNewSearch()}>
                <PlusOutlined className="newSearchIcon" style={{fontSize: "1.4rem", marginBottom: "2px"}}/> <p>Pencarian baru</p>
            </button>

            <button className="downloadButton btn btn-round btn-primary" onClick={(e) => handleClick()}>
                <DownloadOutlined className="downloadIcon" style={{fontSize: "1.4rem", marginBottom: "2px"}}/> <p>Unduh hasil pencarian</p>
            </button>
            </div>
        </>
    )
}