import React from "react";
import "./avatar.css";

class Avatar1 extends React.Component {
    render() {

    return (
        <>
            <div className="avatarContainer">
                <img src="https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/batman_hero_avatar_comics-512.png" alt="Avatar"/>
            </div>
        </>
    )
    }
}

class Avatar2 extends React.Component {
    render() {

    return (
        <>
            <div className="avatarContainer">
                <img src="https://media-exp1.licdn.com/dms/image/C4E0BAQG0XeimSIYLJA/company-logo_200_200/0/1605557412229?e=2147483647&v=beta&t=JgYw9kImrvuEpgxEQf9jDwtsmC543KJ2cO1tSwXSy0s" alt="Avatar"/>
            </div>
        </>
    )
    }
}

export {Avatar1, Avatar2};