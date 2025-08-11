import React, { useContext, useEffect, useState } from "react";
import { Avatar1 } from "../../assets/avatar/avatar";
import {
    FormGroup,
    Label,
    Input,
    FormText,
    Button,
    UncontrolledTooltip
  } from "reactstrap";
import { Col, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import {
    QuestionCircleOutlined, ThunderboltFilled
  } from '@ant-design/icons';


import "./landing.css"
import LoginModal from "./modals/userLogin";
import AdvancedSettingsModal from "./modals/advancedSettings";
import { UserContext } from "context/userContext";
import Parse from 'parse/dist/parse.min.js';
import { ProcessContext } from "context/processContext";
import { SummaryContext } from "context/summaryContext";
import { useNavigate } from "react-router-dom";
import { SearchParamContext } from "context/modalContext";

export default function LandingPage(){

    const {userContext, setUserContext} = useContext(UserContext);
    const {processContext, setProcessContext} = useContext(ProcessContext);
    const {summaryContext, setSummaryContext} = useContext(SummaryContext);
    const {searchParamContext} = useContext(SearchParamContext);
    const [userLocation, setUserLocation] = useState("")
    const [showModal, setShowModal] = useState(false)
    const [query, setQuery] = useState("")
    const [minPrice, setMinPrice] = useState("")
    const [maxPrice, setMaxPrice] = useState("")
    const [modal, setModal] = useState(false);

    const [blibliParam, setBlibliParam] = useState("");
    const [bukalapakParam, setBukalapakParam] = useState("");
    const [shopeeParam, setShopeeParam] = useState("");
    const [tokopediaParam, setTokopediaParam] = useState("");

    const toggle = () => setModal(!modal);

    const navigate = useNavigate()

    // Your Parse initialization configuration goes here
    const PARSE_APPLICATION_ID = 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI';
    const PARSE_HOST_URL = 'https://parseapi.back4app.com/';
    const PARSE_JAVASCRIPT_KEY = 'C1PFzXvctEIjXA33a1rYy68fxdfh3bBlXzLBNEaC';
    Parse.initialize(PARSE_APPLICATION_ID, PARSE_JAVASCRIPT_KEY);
    Parse.serverURL = PARSE_HOST_URL;

    // GEOLOCATION FUNCTION
    const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };
    
    function success(pos) {
        const crd = pos.coords;
        const userLocationGet = {
            'lat': crd.latitude,
            'lon': crd.longitude,
            'acc': crd.accuracy
        }
        
        setUserLocation(userLocationGet)
    }
    
    function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    } 

    // Save user input
    async function addQuery(userContext) {

        let blibliParam_, bukalapakParam_, shopeeParam_, tokopediaParam_

        {userContext.searchParam.blibli != "" ? blibliParam_ = ""+userContext.searchParam.blibli : blibliParam_ = "20"}
        {userContext.searchParam.bukalapak != "" ? bukalapakParam_ = ""+userContext.searchParam.bukalapak : bukalapakParam_ = "20"}
        {userContext.searchParam.shopee != "" ? shopeeParam_ = ""+userContext.searchParam.shopee : shopeeParam_ = "20"}
        {userContext.searchParam.tokopedia != "" ? tokopediaParam_ = ""+userContext.searchParam.tokopedia : tokopediaParam_ = "20"}

        try {
            // create a new Parse Object instance
            const QueryPost = new Parse.Object('Queries');
            // define the attributes you want for your Object
            QueryPost.set('lat', userContext.userLocation.lat + "");
            QueryPost.set('long', userContext.userLocation.lon + "");
            QueryPost.set('query', userContext.userInput.query);
            QueryPost.set('price_max', userContext.userInput.maxPrice);
            QueryPost.set('price_min', userContext.userInput.minPrice);
            QueryPost.set('searchParam_blibli', blibliParam_);
            QueryPost.set('searchParam_bukalapak', bukalapakParam_);
            QueryPost.set('searchParam_shopee', shopeeParam_);
            QueryPost.set('searchParam_tokopedia', tokopediaParam_);
            // save it on Back4App Data Store
            await QueryPost.save();
            const QueryGet = new Parse.Query('Queries');
            QueryGet.contains('query', userContext.userInput.query);
            QueryGet.contains('price_max', userContext.userInput.maxPrice);
            QueryGet.contains('price_min', userContext.userInput.minPrice);

            const queryResults = await QueryGet.find();

            const QueryId = await queryResults[queryResults.length-1].id;
            return QueryId;
        
        } catch (error) {
            console.log('Error saving new query: ', error);
        }
    }

    // async function getData_blibli(queryId) {
    //     console.log('blibli')
    //     const res_blibli = await fetch('https://ecommercemonitor.herokuapp.com/search/_blibli/' + queryId, {
    //                                     method: 'GET',
    //                                     headers: {
    //                                     accept: 'application/json',
    //                                     },
    //                                 })
    //     const data_blibli = await res_blibli.json();
    //     return data_blibli
    // }

    // async function getData_bukalapak(queryId) {
    //     console.log('bukalapak')
    //     const res_bukalapak = await fetch('https://ecommercemonitor.herokuapp.com/search/_bukalapak/' + queryId, {
    //                                         method: 'GET',
    //                                         headers: {
    //                                         accept: 'application/json',
    //                                         },
    //                                     })
    //     console.log(res_bukalapak)
    //     const data_bukalapak = await res_bukalapak.json();
    //     return data_bukalapak
    // }

    // async function getData_shopee(queryId) {
    //     console.log('shopee')
    //     const res_shopee = await fetch('https://ecommercemonitor.herokuapp.com/search/_shopee/' + queryId, {
    //                                     method: 'GET',
    //                                     headers: {
    //                                     accept: 'application/json',
    //                                     },
    //                                 })
    //     const data_shopee = await res_shopee.json();
    //     return data_shopee
    // }

    // async function getData_tokopedia(queryId) {
    //     console.log('tokopedia')
    //     const res_tokopedia = await fetch('https://ecommercemonitor.herokuapp.com/search/_tokopedia/' + queryId, {
    //                                         method: 'GET',
    //                                         headers: {
    //                                         accept: 'application/json',
    //                                         },
    //                                     })
    //     const data_tokopedia = await res_tokopedia.json();
    //     return data_tokopedia
    // }

    // Connect to Python
    async function getData(queryId) {

        // let [blibli_items, bukalapak_items, shopee_items, tokopedia_items] = await Promise.all([
        //     getData_blibli(queryId),
        //     getData_bukalapak(queryId),
        //     getData_shopee(queryId),
        //     getData_tokopedia(queryId)])

        let res_dict = {}

        // const res_blibli = await fetch('/search/' + queryId);
        // const data_blibli = await res_blibli.json();
        // res_dict['blibli'] = data_blibli

        // res_dict['blibli'] = blibli_items

        // const res_bukalapak = await fetch('/search/' + queryId);
        // const data_bukalapak = await res_bukalapak.json();
        // res_dict['bukalapak'] = data_bukalapak

        // res_dict['bukalapak'] = bukalapak_items

        // const res_shopee = await fetch('/search/' + queryId);
        // const data_shopee = await res_shopee.json();
        // res_dict['shopee'] = data_shopee

        // res_dict['shopee'] = await shopee_items
        
        // const res_tokopedia = await fetch('/search/' + queryId);
        // const data_tokopedia = await res_tokopedia.json();
        // res_dict['tokopedia'] = data_tokopedia

        // res_dict['tokopedia'] = await tokopedia_items

        const res = await fetch('/search/' + queryId);
        const data = await res.json();
        res_dict = data
        
        setSummaryContext(res_dict)
        setProcessContext(queryId)
        return summaryContext;
    }

    // Update context once we have an update on query
    useEffect(() => {
        setUserContext(
            {
                'userInput': {
                    'query': query,
                    'minPrice': minPrice,
                    'maxPrice': maxPrice
                },
                'userLocation': {
                    'lat': userLocation.lat,
                    'lon': userLocation.lon,
                    'acc': userLocation.acc
                },
                'searchParam': {
                    'blibli': blibliParam,
                    'bukalapak': bukalapakParam,
                    'shopee': shopeeParam,
                    'tokopedia': tokopediaParam
                }
            }
        )
    }, [query, minPrice, maxPrice, userLocation, blibliParam, bukalapakParam, shopeeParam, tokopediaParam])

    useEffect(() => {
        try {
            navigator.geolocation.getCurrentPosition(success, error, options);
        } catch (e) {
            setUserLocation(getLocation())
        }
    }, [])

    async function getLocation(){
        const res = await fetch('https://geolocation-db.com/json/')
        const data = await res.json()
        const userLocationGet = {
            'lat': data.latitude,
            'lon': data.longitude
        }
        return userLocationGet
    }
      
    // Handle search -> save user input
    async function handleClick(){
        const queryId = await addQuery(userContext)
        setQuery("")
        setMinPrice("")
        setMaxPrice("")
        setSummaryContext(null)
        navigate('/loading')
        return getData(queryId)
    }

  return (
      <div className="landingPageContainer">
        {/* ECM Logo as a header */}
        <div className="ecmLogoContainer">
            <div className="ecmLogo ecmLogoImg">
                <Avatar1/>
            </div>
            <div className="ecmLogo ecmLogoWord">
                <h5>E-COMMERCE</h5>
                <h5>MONITOR</h5>
            </div>
        </div>
        {/* Container for user inputted values. Use simple and minimum form columns, except for collapsable advanced search settings */}
        <div className="inputContainer">
            <form>
                {/* Input form for search query - Public */}
                <FormGroup>
                    <Label for="formSearchQuery">Keyword:</Label>
                    <Input
                        type="text"
                        name="searchQuery"
                        id="searchQuery"
                        placeholder="Enter keyword"
                        onChange={(e) => setQuery(e.target.value)}
                        value={query}
                    />
                    <FormText color="muted">
                        Tulis barang yang kamu cari disini
                    </FormText>
                </FormGroup>
            
                <hr/>

                {/* Input form for users' price estimation - Public */}
                <Label for="estPrice">Estimasi harga (opsional):</Label>
                    <div className="formPriceEstimation">
                        <FormText color="muted">
                            Dari
                        </FormText>
                        <Input
                            type="number"
                            name="estPrice"
                            id="minPrice"
                            placeholder="Rp..."
                            className="priceInput"
                            onChange={(e) => setMinPrice(e.target.value)}
                            value={minPrice}
                        />
                        <FormText color="muted">
                            hingga
                        </FormText>
                        <Input
                            type="number"
                            name="estPrice"
                            id="maxPrice"
                            placeholder="Rp..."
                            className="priceInput"
                            onChange={(e) => setMaxPrice(e.target.value)}
                            value={maxPrice}
                        />

                        {/* Popup that explains this is optional */}
                        <QuestionCircleOutlined id="estimationTooltip"/>
                        <UncontrolledTooltip placement="right" target="estimationTooltip" delay={0.2}>
                            Estimasi harga barang yang kamu cari
                        </UncontrolledTooltip>
                    </div>
            </form>
        </div>

        <div className="landingPageButtons">
            {/* Advanced settings form - Premium only */}
            {/* <div className="landingPageButton formAdvancedSearchSettings"> */}
                {/* Button that shows modal to advanced settings */}
                <button className="btn btn-round btn-primary btn-advanceSettings" onClick={(e) => setModal(true)}>Advanced Settings</button>
                {/* {isLogin ? 
                // Modal: if user is premium, then show modal with advanced search settings
                <AdvancedSettingsModal/> :
                // Modal: if user is Public, then show modal with restriction notice and redirect link for premium sign up page
                <LoginModal/> */}
            {/* </div> */}
                
            <button className="landingPageButton btn btn-round btn-primary" onClick={(e) => handleClick()}>Search</button>
        </div>

        <Modal isOpen={modal} toggle={toggle}>
            <ModalHeader toggle={toggle}>Advanced search settings</ModalHeader>
                <ModalBody>
                <FormGroup row>
                    <Label
                    for="BliBliParam"
                    sm={2}
                    >
                    Blibli
                    </Label>
                    <Col sm={10}>
                    <Input
                        id="BliBliParam"
                        name="blibliParam"
                        placeholder="e.g., 20"
                        type="number"
                        value={blibliParam}
                        onChange={(e) => setBlibliParam(e.target.value)}
                    />
                    </Col>
                </FormGroup>
                <FormGroup row>
                    <Label
                    for="BukalapakParam"
                    sm={2}
                    >
                    Bukalapak
                    </Label>
                    <Col sm={10}>
                    <Input
                        id="BliBliParam"
                        name="bukalapakParam"
                        placeholder="e.g., 20"
                        type="number"
                        value={bukalapakParam}
                        onChange={(e) => setBukalapakParam(e.target.value)}
                    />
                    </Col>
                </FormGroup>
                <FormGroup row>
                    <Label
                    for="ShopeeParam"
                    sm={2}
                    >
                    Shopee
                    </Label>
                    <Col sm={10}>
                    <Input
                        id="ShopeeParam"
                        name="shopeeParam"
                        placeholder="e.g., 20"
                        type="number"
                        value={shopeeParam}
                        onChange={(e) => setShopeeParam(e.target.value)}
                    />
                    </Col>
                </FormGroup>
                <FormGroup row>
                    <Label
                    for="TokopediaParam"
                    sm={2}
                    >
                    Tokopedia
                    </Label>
                    <Col sm={10}>
                    <Input
                        id="TokopediaParam"
                        name="tokopediaParam"
                        placeholder="e.g., 20"
                        type="number"
                        value={tokopediaParam}
                        onChange={(e) => setTokopediaParam(e.target.value)}
                    />
                    </Col>
                </FormGroup>
                </ModalBody>
            <ModalFooter>
                <Button color="primary" onClick={(toggle)}>
                    Simpan
                </Button>{' '}
            </ModalFooter>
        </Modal>

      </div>
  )
}