import { format, isValid } from 'date-fns';
import { ETimeInterval } from '@compound/ModeSelector/ModeSelector';

export const dateLabelFormatter = (
    dateString: string,
    interval: ETimeInterval
) => {
    const date = new Date(dateString);

    if (isValid(date)) {
        switch (interval) {
            case ETimeInterval.MINUTE:
                return `${format(date, 'MMM dd')} \n${format(date, 'HH:mm')}`;
            case ETimeInterval.HOUR:
                return format(date, 'MMM dd HH:mm');
            case ETimeInterval.DAY:
                return format(date, 'MMM dd');
            case ETimeInterval.MONTH:
                return format(date, 'MMM yyyy');
            case ETimeInterval.YEAR:
                return format(date, 'yyyy');
        }
    }

    return dateString;
};
