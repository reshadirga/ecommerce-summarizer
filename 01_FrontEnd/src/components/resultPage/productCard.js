import { CaretDownFilled, CaretDownOutlined, DownOutlined } from "@ant-design/icons";
import React, { useContext, useEffect, useState } from "react";
import { Accordion, AccordionBody, AccordionHeader, AccordionItem, Button, Card, CardBody, CardSubtitle, CardTitle, Tooltip } from "reactstrap";
import './productCard.css'
import ProductCardEmpty from "./productCardEmpty";

export default function ProductCard(props){

    const productDetails_json = JSON.parse(props.product);
    const [rotateChevron, setRotateChevron] = useState(false);
    const [open, setOpen] = useState('');
    const [tooltipOpen, setTooltipOpen] = useState(false);
    const productDetails = productDetails_json[0];

    let title = null;
    let price = null;
    let rating = null;
    let sold = null;
    let review = null;
    let location = null;
    let thumbnail = null;
    let url = null;

    try {
        title = productDetails.title;
        price = productDetails.price_display;
        rating = productDetails.rating;
        sold = productDetails.sold;
        review = productDetails.review;
        location = productDetails.location;
        thumbnail = productDetails.thumbnail;
        url = productDetails.url;

        if (rating == null) rating = 'unknown'
        if (sold == null) sold = 'unknown'
        if (review == null) review = 'unknown'
        if (location == null) location = 'unknown'
    } catch (e) {
        console.log(e)   
    }


        const handleRotate = () => setRotateChevron(!rotateChevron);
        const rotate = rotateChevron ? "rotate(180deg)" : "rotate(0)"

        const toggle = (id) => {
            if (open === id) {
            setOpen();
            } else {
            setOpen(id);
            } };

        const toggle_toolTip = () => setTooltipOpen(!tooltipOpen);

        function truncate(text) {
            if (text.length > 35) {
                return text.substring(0, 32) + '...';
            }
            return text;
        }

    return (
        <>
        {
            title ?
            <Card
            style={{
                minWidth: "20rem",
                width: "10vw",
                minHeight: "12rem"
            }} className="cardContainer"
            >
                <img
                    alt={truncate(title)}
                    src={thumbnail}
                    className="productImg"
                    />
                <CardBody>
                    <Accordion flush open={open} toggle={toggle}>
                        <CardTitle tag='p' className="cardTitle" id={'ToolTip' + props.id}>
                            {truncate(title)}
                        </CardTitle>
                        <Tooltip
                            isOpen={tooltipOpen}
                            toggle={toggle_toolTip}
                            target={'ToolTip' + props.id}
                            >
                            {title}   
                        </Tooltip>
                        <CardSubtitle
                            className="mb-2 text-muted"
                            tag="p"
                            >
                            {price}
                        </CardSubtitle>
                        <AccordionItem>
                            <AccordionHeader targetId="1" tag={"div"}>
                                <p style ={{fontSize: "0.7rem", fontWeight: "300", marginRight: '5px'}}>More details</p> <CaretDownOutlined style={{ transform: rotate, transition: "all 0.3s linear" }} onClick={handleRotate} />
                            </AccordionHeader>
                            <AccordionBody accordionId="1">
                                <p>Rating: {rating}</p>
                                <p>Sold: ~{sold}</p>
                                <p>Reviews: {review}</p>
                                <p>Location: {location}</p>
                            </AccordionBody>
                        </AccordionItem>
                    </Accordion>
                    <Button className="goToPageButton btn-round btn-primary">
                        <a target={"_blank"} href={url} className="buttonText">To page</a>
                    </Button>
                </CardBody>
            </Card> :
            <ProductCardEmpty className="cardContainer"/>    
        }
        </>
    )
    }