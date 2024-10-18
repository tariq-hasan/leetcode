import { AgGridColumnProps } from 'ag-grid-react';
import axios, { CancelTokenSource } from 'axios';
import {
    IServerSideDatasource,
    IServerSideGetRowsParams
} from 'ag-grid-community';

const API_BASE_URL = '/api/v1';
const ERROR_SCHEMA = [{
    headerName: 'Error',
    field: 'error',
    colId: 'error'
}];

type SchemaSetter = (schema: AgGridColumnProps[]) => void;
type MetadataSetter = (metadata: AgGridColumnProps[]) => void;

interface RecordType {
    AXIS1: string;
    AXIS2: string;
    AXIS3: string;
    AXIS4: string;
    CURRENCY: string;
    DATA_CONVENTION: string;
    INSTANCE: string;
    Index1: string;
    Index2: string;
    Index3: string;
    Index4: string;
    MARKET_DATA_TYPE: string;
    ModelEnvironment: string;
    ProductClass: string;
    SourceSystem: string;
    model_elt_def_type: string;
    model_env: string;
    source_system: string;
}

// interface Records {
//     records: RecordType[];
//     schema?: AgGridColumnProps[];
//     metadata_schema?: AgGridColumnProps[];
// }

class ServerSideDataSource implements IServerSideDatasource {
    private setSchema?: SchemaSetter;
    private setMetadataSchema?: MetadataSetter;
    private initialized: boolean;
    private sourceSystemName: string | undefined;
    private sourceSystemModelEnv: string | undefined;
    private totalRows: number;
    private source: CancelTokenSource;

    constructor() {
        this.initialized = false;
        this.totalRows = 0;
        this.source = axios.CancelToken.source();
        // this.sourceSystemName = undefined;
        // this.sourceSystemModelEnv = undefined;
    }

    /** Resets the datasource to its initial state and returns a new instance. */
    reset(): void {
        this.initialized = false;
        this.totalRows = 0;
        this.setSchema = undefined;
        this.setMetadataSchema = undefined;
        this.sourceSystemName = undefined;
        this.sourceSystemModelEnv = undefined;
        // return new ServerSideDataSource();
    }

    /** Sets the source system name and model environment. */
    setSourceSystem(
        sourceSystemName: string,
        sourceSystemModelEnv: string
    ): void {
        this.sourceSystemName = sourceSystemName;
        this.sourceSystemModelEnv = sourceSystemModelEnv;
    }

    /** Checks if the datasource has been initialized. */
    isInitialized(): boolean {
        return this.initialized;
    }

    /** Updates the initialization status based on schema presence. */
    private updateInitializationStatus(): void {
        this.initialized = !!(this.setSchema && this.setMetadataSchema);
    }

    /** Sets the schema setter and updates initialization status. */
    setSchemaSetter = (setter: SchemaSetter): void => {
        if (typeof setter !== "function") {
            console.error("setSchemaSetter expects a function.");
            return;
        }
        this.setSchema = setter;
        this.updateInitializationStatus();
    };

    /** Sets the metadata schema setter and updates initialization status. */
    setMetadataSchemaSetter = (setter: MetadataSetter): void => {
        if (typeof setter !== "function") {
            console.error("setMetadataSchemaSetter expects a function.");
            return;
        }
        this.setMetadataSchema = setter;
        this.updateInitializationStatus();
    };

    /** Get the source system name. */
    getSourceSystemName(): string | undefined {
        return this.sourceSystemName;
    }

    /** Get the source system model environment. */
    getSourceSystemModelEnv(): string | undefined {
        return this.sourceSystemModelEnv;
    }

    /**
     * Utility function to extract records.
     * @param data The raw data from the server response
     * @returns An array of extracted records
     */
    private extractRecords(data: any[]): RecordType[] {
        return data
            .filter((item: any) => Array.isArray(item.data) && item.data.length > 0)
            .map((item: any) => item.data[0] as RecordType);
    }

    /**
     * Detects the appropriate filter type for a given value.
     * @param value - The value for which the filter type needs to be determined.
     * @returns A string representing the filter type, which can be one of 
     *          'agNumberColumnFilter', 'agSetColumnFilter', 'agDateColumnFilter',
     *          or 'agTextColumnFilter'.
     */
    private detectFilterType(value: any): string {
        const filterConditions: { [key: string]: (val: any) => boolean } = {
            'agNumberColumnFilter': (val: any) => typeof val === 'number',
            'agSetColumnFilter': (val: any) => typeof val === 'boolean',
            'agDateColumnFilter': (val: any) => typeof val === 'string' && /^\d{4}-\d{2}-\d{2}/.test(val),
            'agTextColumnFilter': (_val: any) => true // Default case (ensure all keys are functions)
        };

        return Object.keys(filterConditions).find((filter) => filterConditions[filter](value)) || 'agTextColumnFilter';
    }

    /**
     * Retrieves the filter parameters for the specified filter type.
     * @param filter - The filter type for which parameters are to be retrieved.
     * @returns An object containing the filter parameters if the filter type is 
     *          'agSetColumnFilter'; otherwise, returns undefined.
     */
    private getFilterParams(filter: string): object | undefined {
        if (filter !== 'agSetColumnFilter') return undefined;
        return { values: ['true', 'false'] };
    }

    /**
     * Updates the schema and metadata schema based on the provided data.
     * This method dynamically generates the schema based on the first record
     * in the data's records array. If a schema exists, it sets the schema
     * and also updates the metadata schema if provided.
     * @param data - The data containing records, schema, and metadata schema.
     */
    private updateSchemas(data: RecordType[]): void {
        if (!this.setSchema) return;

        const firstRecord = data[0] ?? {};

        const defaultSchemaProps = {
            hide: false,
            filterParams: undefined,
        };

        const newSchema = Object.keys(firstRecord).map((field) => {
            const fieldValue = firstRecord[field as keyof RecordType];
            const filter = this.detectFilterType(fieldValue);
        
            return {
                ...defaultSchemaProps,
                headerName: field.replace(/_/g, ' ').toUpperCase(),
                field: field,
                colId: field,
                filter: filter,
                filterParams: this.getFilterParams(filter),
            };
        });

        this.setSchema(newSchema);
        console.debug("Generated schema:", JSON.stringify(newSchema, null, 2));

        // if (this.setMetadataSchema && data.metadata_schema) {
        //     this.setMetadataSchema(data.metadata_schema);
        // }
    }

    /**
     * Handles errors and sets error data for the grid.
     * @param errorMsg The error message to display
     * @param params ag-grid server-side row parameters
     */
    private handleError(errorMsg: string, params: IServerSideGetRowsParams): void {
        if (this.setSchema) {
            this.setSchema(ERROR_SCHEMA);
        }
        if (this.setMetadataSchema) {
            this.setMetadataSchema([]);
        }
        params.success({
            rowData: [{ error: errorMsg }],
            rowCount: 1,
        });
    }

    /**
     * Fetches rows from the server for AG Grid based on user interactions.
     * @param params - AG Grid parameters containing pagination (startRow, endRow) and filters.
     * @returns A Promise that resolves to void. It updates the grid using provided success or failure callbacks.
     * @throws Calls params.success with an error message if the source system name is not defined or if data retrieval fails.
     */
    async getRows(params: IServerSideGetRowsParams): Promise<void> {
        try {
            console.debug("Request params:", JSON.stringify(params.request, null, 2));
    
            // Cancel previous request if active
            if (this.source) {
                this.source.cancel("Operation canceled due to new request.");
            }
            this.source = axios.CancelToken.source();

            // Ensure source system name is defined
            if (!this.sourceSystemName) {
                return this.handleError("Source system is not defined", params);
            }

            // Extract startRow and endRow from params.request
            const { startRow, endRow } = params.request;
            const url = `${API_BASE_URL}/get_rf_name/${this.sourceSystemName}/${this.sourceSystemModelEnv}/`;

            // Send GET request with pagination params
            const response = await axios.get(url, {
                cancelToken: this.source.token,
                params: {
                    offset: startRow,
                    limit: endRow - startRow,
                },
            });

            // Log and handle data
            const { data } = response;
            console.debug("Response data:", data);

            if (!data || data.length === 0) {
                params.api.showNoRowsOverlay();
                return params.success({ rowData: [], rowCount: 0 });
            }

            // Extract records and update schemas
            const records = this.extractRecords(data);
            this.updateSchemas(records);

            // Send successful response back to AG Grid
            params.success({ rowData: records, rowCount: data.length });

            } catch (error: unknown) {
                console.error("Error fetching data:", error);
                const errorMessage = error instanceof Error 
                    ? `Could not fetch data: ${error.message}` 
                    : `Could not fetch data: ${String(error)}`;
                this.handleError(errorMessage, params);
            }
        }
    }

export default ServerSideDataSource;
