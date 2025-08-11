import { CaretDownFilled, CaretDownOutlined, DownOutlined } from "@ant-design/icons";
import React, { useContext, useEffect, useState } from "react";
import { Accordion, AccordionBody, AccordionHeader, AccordionItem, Button, Card, CardBody, CardSubtitle, CardTitle, Tooltip } from "reactstrap";
import './productCard.css'

export default function ProductCardEmpty(){


    return (
        <Card
        style={{
            minWidth: "20rem",
            width: "20vw",
            minHeight: "12rem"
        }}
        >
            <CardBody>
                <CardTitle
                    className="mb-2 text-muted"
                    tag="p"
                    >
                    Tidak dapat menganalisa barang
                </CardTitle>
            </CardBody>
        </Card>
    )
}