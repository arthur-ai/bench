export enum ComparatorType {
    GREATER_THAN_EQUAL = 'gte',
    GREATER_THAN = 'gt',
    LESS_THAN = 'lt',
    LESS_THAN_EQUAL = 'lte',
    EQUAL = 'eq',
    NOT_EQUAL = 'ne',
    LIKE = 'like',
    IN = 'in',
    NOT_NULL = 'NotNull',
}

export const comparatorLangMap: Record<string, string> = {
    gt: 'greater than',
    gte: 'greater than or equal to',
    lt: 'less than',
    lte: 'less than or equal to',
    eq: 'equal to',
    ne: 'not equal to',
    like: 'like',
    in: 'in',
    NotNull: 'not null',
};

export const ComparatorTypeMap = {
    gt: ComparatorType.GREATER_THAN,
    gte: ComparatorType.GREATER_THAN_EQUAL,
    lt: ComparatorType.LESS_THAN,
    lte: ComparatorType.LESS_THAN_EQUAL,
    eq: ComparatorType.EQUAL,
    ne: ComparatorType.NOT_EQUAL,
    like: ComparatorType.LIKE,
    in: ComparatorType.IN,
    NotNull: ComparatorType.NOT_NULL,
};
