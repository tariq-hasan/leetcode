import React, { useState, useEffect } from 'react'
import { AgGridReact, AgGridColumn, AgGridColumnProps } from 'ag-grid-react'
import {
    GridReadyEvent,
    ServerSideStoreType,
    ValueFormatterParams,
    RowEditingStartedEvent,
    RowEditingStoppedEvent,
    GridApi
} from 'ag-grid-community'
import 'ag-grid-enterprise'
import ServerSideDataSource from './ServerSideDataSource'
import RecordCellRenderer from './renderers/RecordCellRenderer'
import ToggleActiveCellRenderer from './renderers/ToggleActiveCellRenderer'

const dataSource = new ServerSideDataSource()

interface Props {
    sourceSystemName: string
    sourceSystemModelEnv: string
    changeset: any
    setChangeset: any
    selectedSourceSystemId: number
    gridApi: GridApi | undefined
    setGridApi: React.Dispatch<React.SetStateAction<GridApi | undefined >>
}

const RiskFactorsGrid: React.FC<Props> = ({
    sourceSystemName,
    sourceSystemModelEnv,
    changeset,
    setChangeset,
    gridApi,
    selectedSourceSystemId,
    setGridApi
}) => {
    const [schema, setSchema] = useState<AgGridColumnProps[]>([])
    const [metadataSchema, setMetadataSchema] = useState<AgGridColumnProps[]>([])
    const [currentEdit, setCurrentEdit] = useState<any>()

    if (!dataSource.isInitialized()) {
        dataSource.setSchemaSetter(setSchema)
        dataSource.setMetadataSchemaSetter(setMetadataSchema)
    }

    useEffect(() => {
        return () => {
            setGridApi(undefined)
            setSchema([])
            setMetadataSchema([])
            setCurrentEdit(undefined)
            dataSource.reset()
        }
    }, [])

    if (
        dataSource.getSourceSystemName() !== sourceSystemName ||
        dataSource.getSourceSystemModelEnv() !== sourceSystemModelEnv
    ) {
        dataSource.setSourceSystem(sourceSystemName, sourceSystemModelEnv)
        if (gridApi) {
            gridApi.refreshServerSideStore({ purge: true })
        }
    }

    const onGridReady = (params: GridReadyEvent) => {
        setGridApi(params.api)
    }

    const jsonFormatter = (params: ValueFormatterParams) => {
        return JSON.stringify(params.data.meta.original_record)
    }

    // Needed to avoid [object object] when copying JSON from the grid
    const processCopy = (params: any) => {
        if (params.column.colId === 'meta.original_record') {
            return JSON.stringify(params.value)
        }
        return params.value
    }

    const onRowEditingStarted = (params: RowEditingStartedEvent) => {
        // Check if node is already in the changeset
        const changesetRow = changeset.find((d: any) => d._key === params.data._key)
        if (changesetRow) {
            setCurrentEdit({ ...changesetRow.original, ...params.data })
        } else {
            setCurrentEdit({ ...params.data, nodeId: params.node.id })
        }
    }

    const onRowEditingStopped = (params: RowEditingStoppedEvent) => {
        if (!gridApi || !params.node.id) {
            return
        }
        // Check if the changeset already has the modified row
        const modifiedRow = gridApi.getRowNode(params.node.id)
        if (!modifiedRow) {
            console.error(`Node ID ${params.node.id} does not exist`)
        }
        const changesetRowIdx = changeset
            .map((d: any) => d._key)
            .indexOf(params.data._key)
        if (changesetRowIdx < 0) {
            // modified row does not exist in the changeset, just append it
            setChangeset((c: any) => [
                ...c,
                {
                    ...params.data,
                    original: currentEdit,
                    modified: params.data,
                    nodeId: params.node.Id
                }
            ])
        } else {
            // Modify the changeset row
            setChangeset((c: any) => [
                ...c.slice(0, changesetRowIdx),
                {
                    ...params.data,
                    original: changeset[changesetRowIdx].original,
                    modified: params.data,
                    nodeId: params.node.id
                },
                ...c.slice(changesetRowIdx + 1, c.length)
            ])
        }
        setCurrentEdit(null)
    }

    return (
        <AgGridReact
            debug={process.env.NODE_ENV === 'development'}
            rowModelType="serverSide"
            serverSideDatasource={dataSource}
            onGridReady={onGridReady}
            serverSideStoreType={ServerSideStoreType.Partial}
            cacheBlockSize={500}
            maxConcurrentDatasourceRequests={3}
            pagination={true}
            paginationPageSize={500}
            paginateChildRows={true}
            processCellForClipboard={processCopy}
            editType="fullRow"
            onRowEditingStarted={onRowEditingStarted}
            onRowEditingStopped={onRowEditingStopped}
            frameworkComponents={{
                RecordCellRenderer,
                ToggleActiveCellRenderer
            }}
            defaultColDef={{
                sortable: false,
                editable: true,
                filter: 'agTextColumnFilter',
                resizeable: true,
                filterParams: { buttons: ['reset', 'apply'] }
            }}
        >
            <AgGridColumn
                headerName="Actions"
                width={100}
                field="meta.is_active"
                sortable={false}
                editable={false}
                cellRenderer="ToggleActiveCellRenderer"
                cellRendererParams = {{selectedSourceSystemId}}
                suppressMenu
            />
            <AgGridColumn headerName="Records">
                {schema &&
                    schema.map((d: AgGridColumnProps) => (
                        <AgGridColumn
                            {...d}
                            key={`ag-grid-header-${sourceSystemName}-${d.headerName}`}
                            cellRenderer="RecordCellRenderer"
                            cellRendererParams={{ changeset, currentEdit }}
                        />
                    ))}
            </AgGridColumn>
            <AgGridColumn headerName="Metadata">
                {metadataSchema &&
                    metadataSchema.map((d: AgGridColumnProps) => (
                        <AgGridColumn
                            {...d}
                            editable={false} // Users are not allowed to edit metadata
                            valueFormatter={
                                d.field === 'meta.original_record' ? jsonFormatter : ''
                            }
                            key={`ag-grid-meta-header-${sourceSystemName}-${d.headerName}`}
                        />
                    ))}
            </AgGridColumn>
        </AgGridReact>
    )
}

export default RiskFactorsGrid
