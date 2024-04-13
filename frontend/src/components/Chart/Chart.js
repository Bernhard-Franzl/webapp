import React from 'react'; //importing the React library
import './Chart.css'; //importing the CSS file for the component

class Chart extends React.Component{
    //constructor method to initialize the state
    constructor(props){
        super(props);
        // defining the states
        this.state = { 
            type: 'Bar',
            children: 'Some nice chart'
        };
        }
    //render method to render the component
    render(){
        return (
            <div>
                <div className="header">
                    <h2>{this.state.type} Chart</h2>
                </div>

                <div className="content">
                    {this.state.children}
                </div>
            </div>
        );
    }
}
export default Chart; //exporting the component so that it can be imported and used in other files