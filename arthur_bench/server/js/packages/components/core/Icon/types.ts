/* eslint-disable no-unused-vars */
import React, { MouseEventHandler } from 'react';
declare global {
    interface Window {
        iconSet: string;
    }
}

export enum EIconType {
    ADD = 'add',
    ADD_CIRCLE = 'add-circle',
    ADD_TAG = 'new-label',
    ALERT = 'alert',
    // API_KEY = 'e92b': See 'Generate'
    ARROW_BACK = 'arrow-back',
    ARROW_DOWN = 'arrow-down',
    ARROW_DOWNWARD = 'arrow-downward',
    ARROW_RIGHT = 'arrow-right',
    ARROW_UPWARD = 'arrow-upward',
    BELL = 'bell',
    BELL_ALERT_OUTLINE = 'bell-alert-outline',
    BULLSEYE = 'bullseye',
    C_SUITE = 'CSuiteMembers',
    CALENDAR = 'calendar',
    CANCEL = 'cancel',
    CANCEL_FILLED = 'cancel-filled',
    CANCEL_ROUND = "cancel-round",
    // CHART = 'chart',
    CHART_OPTION_2 = 'insights',
    CHART_VIEW_SETTINGS = 'tune',
    CHAT = 'chat',
    CHAT_FILLED = 'chat-filled',
    CHEVRON_DOWN = 'expand-more-black-24dp',
    CHEVRON_LEFT = 'chevron-left',
    CHEVRON_RIGHT = 'chevron-right',
    CHEVRON_UP = 'expand-less-black-24dp',
    CIRCLE_LEFT = 'circle-left',
    CIRCLE_RIGHT = 'circle-right',
    CLOSE_CIRCLE = 'cancel',
    CODE_BRIEFCASE = 'integration-instructions',
    CODE_BRIEFCASE_FILLED = 'integration-instructions-filled',
    COMMUNITY = 'forum',
    COPY = 'copy',
    CRITICAL = 'report',
    DATA_SCIENTIST = 'DataScientist',
    DATA_SECURITY = 'DataSecurity',
    DELETE = 'delete',
    // DELETE_ITEM = 'delete_item',
    DELETE_OUTLINED = 'delete-item',
    DEM_ML = 'DemocratizeMLperformance',
    DOCUMENTATION = 'article',
    DONE = 'done',
    // DUPLICATED = 'duplicated',
    // DROP_DOWN = 'arrow_drop_down',
    // EDIT = 'edit': See 'PENCIL'
    ERROR = 'error',
    EXPLAINABILITY = 'Explainability',
    EXPORT = 'export',
    EXTERNAL_LINK = 'launch',
    FAIRNESS = 'Fairness',
    FILTER = 'filter',
    FINANCE = 'finance',
    FINANCIAL_SERVICES = 'FinancialServices',
    FLAG = 'flag',
    FOLDER_SETTINGS_OUTLINE = 'folder-settings-outline',
    GROWTH = 'Growth',
    HAND = 'hand',
    HEALTH_INSURANCE = 'HealthInsurance',
    HELP = 'help',
    HIDE = 'hide',
    HOME = 'home',
    // HOVER = 'hover',
    I18N = 'localization',
    INCREASE = 'IncreaseIcon',
    INFO = 'info',
    INFORMATION = 'information',
    INSIGHTS = 'ActionableInsights',
    LIGHTBULB = 'lightbulb-on',
    // LOCALIZATION = 'localization': See 'I18N'
    LOGOUT = 'logout',
    MAIL = 'email',
    ML_GOVERNANCE = 'StrengthenMLGovernance',
    // MORE = 'more-vert': See 'OPTIONS'
    NONE = 'none',
    NOTEBOOK = 'sticky_note_2',
    NOTE_EDIT_OUTLINE = 'note-edit-outline',
    NOTE_WRITE = 'note-write',
    OPTIONS = 'options',
    PENCIL = 'pencil',
    PENCIL_BOX = 'pencil-box-multiple-outline',
    PENCIL_BOX_MULTIPLE_OUTLINE = 'pencil-box-multiple-outline1',
    PERFORMANCE = 'Performance',
    PLAY = 'play-circle-filled',
    PRODUCT_MANAGERS = 'ProductManagers',
    RD = 'RD',
    REMOVE = 'remove',
    REPLAY = 'replay',
    RETAIL = 'Retail',
    RISK_AND_COMPLIANCE = 'RiskandCmplianceOfficers',
    SCALABILITY = 'Scalability',
    SEARCH = 'search',
    SEGMENTATION = 'segmentation',
    SEND = 'send',
    SHAPE = 'shape',
    // SHOW = 'show': See 'DETAILS'
    SORT_ASC = 'sort-asc',
    SORT_DEFAULT = 'sort-default',
    SORT_DESC = 'sort-desc',
    SUCCESS = 'success',
    TAG = 'tag',
    // TAGS = 'tags',
    TECH = 'Tech',
    TOUR = 'rocket-launch',
    UPDATE = 'update',
    ZOOM = 'zoom-in',
    ZOOM_OUT = 'zoom-out',
    ZOOM_RESET = 'Vector',
    //Input Type Icons
    COMPUTER_VISION = 'computer-vision',
    NLP_DATA = 'nlp',
    TABULAR_DATA = 'tabular-data',
    //Output Type Icons
    CLASSIFICATION = 'classification',
    DETAILS = 'details',
    GENERATE = 'generate',
    GLOBAL_FILTER = 'global-filter',
    MULTILABEL = 'multilabel',
    NLP = 'NaturalLanguageProcessing1',
    OBJECT_DETECTION = 'object-detection',
    REGRESSION = 'regression',
    SCHEMA = 'schema',
    SHOW_CHART = 'show-chart',
    COLLAPSE = 'collapse',
    EXPAND = 'expand',
    POINTER = 'pointer',
    WORKSPACE ='workspace'
}

export type TIconProps = {
    color?: string;
    size: string | number;
    icon: EIconType;
    style?: React.CSSProperties;
    className?: string;
    clickHandler?: MouseEventHandler;
    ref?: React.RefObject<HTMLElement>;
    testId?: string;
};
