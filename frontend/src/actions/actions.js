export const t = {
    STORE_PREDICTIONS: "STORE_PREDICTIONS",
    TOGGLE_EXPLANATION: "TOGGLE_EXPLANATION",
    UPDATE_ARTICLE_TEXT: "UPDATE_ARTICLE_TEXT",
};

export const actions = {
    storePredictions: payload => ({
        type: t.STORE_PREDICTIONS,
        payload,
    }),

    toggleExplanation: () => ({
        type: t.TOGGLE_EXPLANATION,
    }),

    updateArticleText: payload => ({
        type: t.UPDATE_ARTICLE_TEXT,
        payload,
    }),
};
