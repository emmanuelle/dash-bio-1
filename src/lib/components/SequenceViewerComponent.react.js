import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactSequenceViewer from 'react-sequence-viewer';

// required according to react-sequence-viewer readme
import jquery from 'jquery';
window.jQuery = jquery;

/**
 *
 */
export default class SequenceViewerComponent extends Component {

    constructor(props) {
	super(props);
	this.props.onMouseSelection = (e) => {
	    e.detail && this.props.setProps({mouseSelection: e.detail});
	}
	this.props.onSubpartSelected = (e) => {
	    e.detail && this.props.setProps({subpartSelected: e.detail});
	}
    }

    componentDidMount() {
	const {coverage,
	       selection,
	       subpartSelected,
	       mouseSelection,
	       setProps} = this.props;
	
	if(coverage) {
	    for(var i = 0; i < coverage.length; i++) {
		const v = i;
		coverage[i].onclick = (e) => {
		    setProps({
			coverageClicked: v
		    });
		}
	    }
	}
	
	setProps({
	    coverage: coverage
	});
    }
    
    shouldComponentUpdate(nextProps, nextState){
	const {
	    showLineNumbers,
	    wrapAminoAcids,
	    charsPerLine,
	    toolbar,
	    search,
	    title,
	    sequenceMaxHeight,
	    badge,
	    coverage,
	    selection,
	    legend
	} = this.props;
	
	if(showLineNumbers != nextProps.showLineNumbers ||
	   wrapAminoAcids != nextProps.wrapAminoAcids ||
	   charsPerLine != nextProps.charsPerLine ||
	   toolbar != nextProps.toolbar ||
	   search != nextProps.search ||
	   title != nextProps.title ||
	   sequenceMaxHeight != nextProps.sequenceMaxHeight ||
	   badge != nextProps.badge ||
	   legend != nextProps.legend 
	  ){
	    return true;
	}

	if(selection != null && nextProps.selection != null){
	    // go through selection
	    for (var propertyName in selection) {
		if(nextProps.selection[propertyName] !==
		   selection[propertyName]){
		    return true;
		}
	    }
	}

	if(coverage != null && nextProps.coverage != null){
	    // go through coverage
	    // save some time by comparing lengths first
	    if(coverage.length != nextProps.coverage.length){
		return true;
	    }
	    // otherwise, go through all of the coverage and compare
	    var i;
	    for(i = 0; i < coverage.length; i++){
		for(var propertyName in coverage[i]) {
		    if(nextProps.coverage[i][propertyName] !==
		       coverage[i][propertyName]){
			return true;
		    }
		}
	    }
	}

	// if everything is the same, do not update
	return false;	
    }
    
    render() {
	
	const id = this.props.id;
	const seq = this.props.sequence;

	const options = {
	    showLineNumbers: this.props.showLineNumbers,
	    wrapAminoAcids: this.props.wrapAminoAcids,
	    charsPerLine: this.props.charsPerLine,
	    toolbar: this.props.toolbar,
	    search: this.props.search,
	    title: this.props.title,
	    sequenceMaxHeight: this.props.sequenceMaxHeight,
	    badge: this.props.badge,
	    onMouseSelection: this.props.onMouseSelection,
	    onSubpartSelected: this.props.onSubpartSelected,
	    coverage: this.props.coverage,
	    selection: this.props.selection,
	    legend: this.props.legend
	};

	if(this.props.coverage){
	    options.coverage = this.props.coverage;
	}
	if(this.props.selection){
	    options.selection = this.props.selection;
	}


	return (
		<div id={id}>
		<ReactSequenceViewer sequence={seq} {...options} />
		</div>
	);
    }
}

SequenceViewerComponent.propTypes = {

    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The amino acid sequence that will be displayed. 
     */ 
    sequence: PropTypes.string,

    /**
     * The option of whether or not to display line numbers.
     */
    showLineNumbers: PropTypes.bool,

    /**
     * The option of whether or not to display the list of amino acids
     * as broken up into separate lines of a fixed length set by 
     * charsPerLine.
     */
    wrapAminoAcids: PropTypes.bool,

    /**
     * The number of amino acids that will display per line.
     */
    charsPerLine: PropTypes.number,

    /**
     * The option of whether or not to display a toolbar at the top
     * that allows the user to choose the number of letters per line.
     */
    toolbar: PropTypes.bool,

    /**
     * The option of whether or not to include a search bar in
     * the header. This supports regex.
     */
    search: PropTypes.bool,

    /**
     * A string that displays at the top of the component.
     */
    title: PropTypes.string,

    /**
     * The maximum height of the sequence; default "400px".
     */
    sequenceMaxHeight: PropTypes.string,

    /**
     * The option of whether or not to display a badge showing the
     * amino acid count at the top of the component beside the title.
     */
    badge: PropTypes.bool,

    /**
     * A highlighted section of the sequence; the color of the highlight 
     * can also be defined. Takes a list of format [min, max, color] where 
     * min is a number that represents the starting index of the selection, 
     * max is a number that represents the stopping index of the selection, 
     * and color is a string that defines the highlight color.
     * Cannot be used at the same time as coverage.
     */
    selection: PropTypes.arrayOf(PropTypes.shape({
	low: PropTypes.number,
	high: PropTypes.number,
	color: PropTypes.string
    })),

    /**
     * A coverage of the entire sequence; each section of the sequence
     * can have its own text color, background color, tooltip (on hover),
     * and an optional underscore. The props start and end represent the
     * beginning and terminating indices of the section in question.
     * Cannot be used at the same time as selection.
     */
    coverage: PropTypes.arrayOf(PropTypes.shape({
	start: PropTypes.number,
	end: PropTypes.number,
	color: PropTypes.string,
	bgcolor: PropTypes.string,
	tooltip: PropTypes.string,
	underscore: PropTypes.bool,
	onclick: PropTypes.func
    })),

    /**
     * A legend corresponding to the color codes above (optionally displayed).
     */
    legend: PropTypes.arrayOf(PropTypes.shape({
	name: PropTypes.string,
	color: PropTypes.string,
	underscore: PropTypes.bool
    })),
	
    
    /**
     * Contains the index of the section that was clicked last in 
     * the coverage.
     */ 
    coverageClicked: PropTypes.number,

    /**
     * A string containing the mouse selection.
     */
    mouseSelection: PropTypes.shape({
	'start': PropTypes.number,
	'end': PropTypes.number,
	'selection': PropTypes.string
    }),

    /**
     * A string containing all of the highlighted sections when 
     * using the search bar.
     */
    subpartSelected: PropTypes.arrayOf(PropTypes.shape({
	'start': PropTypes.number,
	'end': PropTypes.number,
	'sequence': PropTypes.string
    })),

    /**
     * A function acting as an event handler for mouse selection. 
     */
    onMouseSelection: PropTypes.func,

    /**
     * A function acting as an event handler for highlight when using
     * the search bar. 
     */
    onSubpartSelected: PropTypes.func,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change.
     */
    setProps: PropTypes.func
}