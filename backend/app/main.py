import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from app.utils.csv_processor import CSVProcessor
from app.services.analysis_engine import AnalysisEngine
from app.services.graph_service import GraphService
from app.models.schemas import AnalysisResponse

app = FastAPI(
    title="Graph-Based Financial Crime Detection Engine - RIFT 2026",
    description="Money Muling Detection using Graph Theory and Temporal Analysis"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store latest analysis result for export
latest_result = None


@app.get("/")
@app.head("/")
async def root():
    """Welcome page with API documentation and quick start guide"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MuleEngine-Pro | RIFT 2026</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
                text-align: center;
            }
            h1 { color: #333; font-size: 2.5em; margin-bottom: 10px; }
            .subtitle { color: #666; font-size: 1.1em; margin-bottom: 30px; }
            .status { 
                background: #10b981; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 20px; 
                display: inline-block;
                margin-bottom: 30px;
                font-weight: bold;
            }
            .links {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 30px;
            }
            .btn {
                padding: 15px 25px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                font-size: 1em;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                font-weight: 600;
            }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
            .btn-primary { background: #667eea; color: white; }
            .btn-secondary { background: #764ba2; color: white; }
            .info { 
                background: #f3f4f6; 
                padding: 20px; 
                border-radius: 8px;
                text-align: left;
                margin-top: 20px;
            }
            .info h3 { color: #333; margin-bottom: 10px; }
            .info code { background: #e5e7eb; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
            .patterns { color: #666; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 MuleEngine-Pro</h1>
            <p class="subtitle">Money Muling Detection Engine | RIFT 2026</p>
            <div class="status">✓ API Online</div>
            
            <div class="links">
                <a href="/docs" class="btn btn-primary">📚 API Docs (Swagger)</a>
                <a href="/redoc" class="btn btn-secondary">📖 ReDoc</a>
            </div>
            
            <div class="info">
                <h3>🎯 Quick Start:</h3>
                <p><strong>Upload a CSV file to analyze transactions:</strong></p>
                <p style="margin: 10px 0;"><code>POST /analyze</code></p>
                <p style="font-size: 0.9em; color: #666;">CSV must include: transaction_id, sender_id, receiver_id, amount, timestamp</p>
                
                <div class="patterns" style="margin-top: 20px;">
                    <strong>Detection Patterns:</strong>
                    <ul style="list-style: none; text-align: center; margin-top: 10px;">
                        <li>🔄 Circular Fund Routing</li>
                        <li>👥 Smurfing Patterns</li>
                        <li>🕸️ Layered Shell Networks</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/analyze")
async def analyze_transactions(file: UploadFile = File(...)):
    """
    RIFT 2026 Hackathon Endpoint
    Upload CSV → Run Full Analysis + Graph Data → Return Combined JSON
    
    CSV Format Required:
    - transaction_id (String)
    - sender_id (String)
    - receiver_id (String)
    - amount (Float)
    - timestamp (YYYY-MM-DD HH:MM:SS)
    """
    global latest_result
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        # 1. Read and Parse CSV
        content = await file.read()
        df = CSVProcessor.parse_csv(content)
        
        # Handle empty dataframe
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty or has no valid transactions.")
        
        print(f"📥 CSV Loaded: {len(df)} transactions")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"📊 Sample row: {df.iloc[0].to_dict() if len(df) > 0 else 'Empty'}")
        
        # 2. Execute Analysis Engine (Stats, Rings, Scores)
        engine = AnalysisEngine(df)
        analysis_result = engine.run_full_analysis()
        
        # 3. Generate Graph Data (Nodes and Edges)
        gs = GraphService(df)
        graph_data = gs.get_graph_json()
        
        # 4. Convert Pydantic model to dict properly
        result_dict = analysis_result.model_dump()
        
        # 5. Merge graph data
        result_dict["graph_data"] = graph_data
        
        # Store for export
        latest_result = result_dict
        
        print(f"✅ Analysis complete: {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges")
        print(f"   Graph nodes: {[n['id'] for n in graph_data['nodes'][:5]]}...")
        print(f"   Graph edges: {graph_data['edges'][:3]}...")
        
        return result_dict

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

@app.get("/export/json")
async def export_json():
    """
    RIFT 2026 Hackathon Export Feature
    Returns the latest analysis result as JSON file download
    Format matches RIFT spec exactly
    """
    global latest_result
    
    if latest_result is None:
        raise HTTPException(status_code=400, detail="No analysis data available. Please run /analyze first.")
    
    # Remove graph_data field for JSON export (per RIFT spec)
    export_data = {
        "suspicious_accounts": latest_result.get("suspicious_accounts", []),
        "fraud_rings": latest_result.get("fraud_rings", []),
        "summary": latest_result.get("summary", {})
    }
    
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": "attachment; filename=mule_detection_results.json"
        }
    )

@app.post("/analyze/graph-data")
async def get_graph_visualization_data(file: UploadFile = File(...)):
    """Legacy endpoint for graph-only analysis"""
    try:
        content = await file.read()
        df = CSVProcessor.parse_csv(content)
        gs = GraphService(df)
        return gs.get_graph_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    # Default port set to 5000 to match frontend dev API (http://localhost:5000)
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)