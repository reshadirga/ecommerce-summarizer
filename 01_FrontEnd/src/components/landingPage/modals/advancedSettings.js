import { SearchParamContext } from "context/modalContext";
import { UserContext } from "context/userContext";
import React, { useContext, useEffect, useState } from "react";
import { Button, Col, FormGroup, Input, Label, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export default function AdvancedSettingsModal(props){

    const {searchParamContext, setSearchParamContext} = useContext(SearchParamContext);
    const {userContext} = useContext(UserContext);
    const [modal, setModal] = useState(props.modal);

    const [blibliParam, setBlibliParam] = useState(20);
    const [bukalapakParam, setBukalapakParam] = useState(20);
    const [shopeeParam, setShopeeParam] = useState(20);
    const [tokopediaParam, setTokopediaParam] = useState(20);

    const toggle = () => setModal(!modal);

    // Update context once we have an update on query
    useEffect(() => {
        setSearchParamContext(
            {
                'blibli': blibliParam,
                'bukalapak': bukalapakParam,
                'shopee': shopeeParam,
                'tokopedia': tokopediaParam
            }
        )
    }, [blibliParam,
        bukalapakParam,
        shopeeParam,
        tokopediaParam])

    return (
        <>
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
                        type="int"
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
                        type="int"
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
                        type="int"
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
                        type="int"
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
        </>
    )
    }