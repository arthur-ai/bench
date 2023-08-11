export enum EInsightStatus {
    NEW = 'new',
    ACKNOWLEDGED = 'acknowledged',
    RESOLVED = 'resolved',
}

type Operator = Record<string, number>;

export type Region = Record<string, Operator>;

export type Insight = {
    id: string;
    model_id: string;
    batch_id: string;
    run_id: string;
    metric_type: string;
    threshold_value: number;
    metric_value: number;
    region: Region;
    timestamp: string;
    status: EInsightStatus;
    inference_count?: number;
};

export interface InsightProps {
    insight: Insight;
    openInferences: (insight: Insight) => void;
}
