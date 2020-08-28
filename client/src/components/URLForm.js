import React, { Component } from "react";

export default class URLForm extends Component {
    constructor() {
        super();

        this.state = {
            short_url: null,
            long_url: null
        }
    }

    handleLongURLChange = (event) => {
        this.setState({long_url: event.target.value});
    }

    handleSubmit = (event) => {
        const requestPayload = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"long_url": this.state.long_url})
        };

        fetch("http://127.0.0.1:8000/api/generate_url/", requestPayload)
            .then(response => response.json())
            .then(json => {
                this.setState({ short_url: json['link'] });
            }
        );

        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}> 
                <div className="form-group">
                    <label htmlFor="long_url">Long URL</label>
                    <input 
                        className="form-control" 
                        type="text" 
                        name="long_url"
                        onChange={this.handleLongURLChange} 
                        placeholder="http://example.com/"
                        required/>
                </div>
                <div className="alert alert-success" role="alert">
                    { this.state.short_url }
                </div>
                <button type="submit" className="btn btn-primary">Generate</button>
            </form>
        );
    }
}
