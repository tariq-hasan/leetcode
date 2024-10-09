
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
    private updateSchemas(data: SchemaData): void {
        if (!this.setSchema) return;

        const firstRecord = data.records?.[0] ?? {};

        const defaultSchemaProps = {
            hide: false,
            filterParams: undefined,
        };

        const newSchema = Object.keys(firstRecord).map((field) => {
            const fieldValue = firstRecord[field];
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

        if (this.setMetadataSchema && data.metadata_schema) {
            this.setMetadataSchema(data.metadata_schema);
        }
    }
