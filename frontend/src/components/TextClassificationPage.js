import React from "react";
import {connect} from "react-redux";
import {actions} from "../actions/actions";

const predictionLabelMapping = {
    'rec.motorcycles': 'motorcycles',
    'comp.sys.mac.hardware': 'mac hardware',
    'talk.politics.misc': 'politics misc',
    'soc.religion.christian': 'christian religion',
    'comp.graphics': 'computer graphics',
    'sci.med': 'medicine',
    'talk.religion.misc': 'misc religion',
    'comp.windows.x': 'windows 10',
    'comp.sys.ibm.pc.hardware': 'pc hardware',
    'talk.politics.guns': 'politics guns',
    'alt.atheism': 'atheism',
    'comp.os.ms-windows.misc': 'windows misc',
    'sci.crypt': 'cryptography',
    'sci.space': 'scientific space',
    'misc.forsale': 'for sale',
    'rec.sport.hockey': 'hockey sport',
    'rec.sport.baseball': 'baseball sport',
    'sci.electronics': 'electronics',
    'rec.autos': 'autos',
    'talk.politics.mideast': 'politics mid-east'
};

export const TextClassificationPageComponent = ({
  prediction,
  topPredictions,
  storePredictions,
  explanationShown,
  toggleExplanation,
  articleText,
  updateArticleText}) => {

    console.log("prediction: ", prediction);

    const classify = () => {
        console.log(articleText);

        fetch('http://localhost:8080/api/classify-article', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({text: articleText})
        }).then(r => r.json())
            .then(r => storePredictions(r['predictions']))
            .catch(e => console.log("error", e))

    };

    const onTextChange = (e) => {
        updateArticleText(e.target.value);
    };

    const onExplanationClick = e => {
        toggleExplanation();
        e.preventDefault();
    };

    return <div className="wrapper">
        <div className="bar">
            <p>Text Classification Page</p>
        </div>

        <div className="user-input-container">
            <textarea type="text" name="user-input" id="user-input" placeholder="Input text to classify..."
                      onChange={onTextChange} defaultValue={articleText}/>
            <button id="classify" name="classify" type="submit" onClick={classify}>Classify</button>
        </div>

        <div className="classification-data-container titles-container">
            <div className="classification-data titles">
                <p className="col-2">Top-3</p>
                <p className="col-2">LABEL</p>
                <p>Probability</p>
            </div>
        </div>

        {topPredictions.map((prediction, index) =>
            <div key={index} className="classification-data-container">
                <div className="classification-data">
                    <p className="col-2">{index + 1}</p>
                    <p className="col-2">{predictionLabelMapping[prediction.label]}</p>
                    <p>{Math.floor(prediction.probability * 100)}%</p>
                    {/*<a id="explanation" href="#" onClick={onExplanationClick}>explain</a>*/}
                </div>
            </div>
        )}


        <div className={`explanation-text-container ${explanationShown ? '' : 'hide'}`}>
            <div className="explanation-text">
                <p className="explanation-title">The most relevant words <span>&#9724;</span></p>
                <p>
                    I'm looking for a replacement radio/tape player for a 1984 Toyota Tercel.
                    Standard off-the-shelf unit is fine, but every place I've gone to (Service Merchandise, etc.)
                    doesn't have my car in its model <span className="highlight">application</span> book.
                    I want to just take out the old radio, and slide in the new, with minimal time spent hooking it up
                    and adjusting the dashboard.If you have put in a new unit in a similar car,
                    I'd like to hear what <span className="highlight">brand</span>, how easy it was to do the change,
                    and any other relevant information. Please answer via E-mail. Thanks,
                    Tom Ostrand
                </p>
            </div>
        </div>

        <footer className="footer">
            <p>Enterprise Data Management WS2017</p>
        </footer>

    </div>
};

const mapStateToProps = (state) => {
    return {
        prediction: state.prediction,
        explanationShown: state.explanationShown,
        topPredictions: state.topPredictions,
        articleText: state.articleText,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        storePredictions: (predictions) => {
            dispatch(actions.storePredictions(predictions))
        },

        toggleExplanation: () => {
            dispatch(actions.toggleExplanation())
        },

        updateArticleText: (text) => {
            dispatch(actions.updateArticleText(text))
        }
    }
};

export const TextClassificationPage = connect(
    mapStateToProps,
    mapDispatchToProps,
)(TextClassificationPageComponent);
