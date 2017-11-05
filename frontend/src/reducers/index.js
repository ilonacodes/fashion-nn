// Set up your root reducer here...
import {combineReducers} from "redux";
import {t} from "../actions/actions";

const emptyReducer = (state = [], action) => {
    return state
};

const predictionReducer = (state = {}, action) => {
    switch (action.type) {
        case t.STORE_PREDICTIONS:
            console.log("all predictions:", action.payload);

            let champion = {label: 'unknown', probability: 0};

            Object.keys(action.payload).forEach(key => {
                if (action.payload[key] > champion.probability) {
                    champion = {label: key, probability: action.payload[key]}
                }
            });

            return champion;

        default:
            return state;
    }
};

const compareFn = (a, b) => {
    if (a.probability > b.probability) {
        return -1;
    }

    if (a.probability < b.probability) {
        return 1;
    }

    return 0;
};

const topPredictionsReducer = (state = [], action) => {
    switch (action.type) {
        case t.STORE_PREDICTIONS:
            return Object.keys(action.payload)
                .map(key => ({
                    label: key,
                    probability: action.payload[key]
                }))
                .sort(compareFn)
                .slice(0, 3);

        default:
            return state;
    }
};

const explanationShownReducer = (state = false, action) => {
    switch (action.type) {
        case t.TOGGLE_EXPLANATION:
            return !state;

        default:
            return state;
    }
};

const articleTextReducer = (state = "", action) => {
    switch (action.type) {
      case t.UPDATE_ARTICLE_TEXT:
        return action.payload;

      default:
        return state;
    }
}

export default combineReducers({
    emptyReducer: emptyReducer,
    prediction: predictionReducer,
    explanationShown: explanationShownReducer,
    topPredictions: topPredictionsReducer,
    articleText: articleTextReducer,
});
