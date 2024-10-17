from flask import Flask, send_file, request, jsonify, send_from_directory, abort, render_template
from flask_cors import CORS
import subprocess
import json
import os
import shutil

app = Flask(__name__, static_folder='fe')
CORS(app)
app.json.ensure_ascii = False


SERVE_DIRECTORY = './fe'

def get_pt_query_digest_path():
    # 首先在 PATH 中查找
    pt_query_digest_path = shutil.which('pt-query-digest')
    if pt_query_digest_path:
        return pt_query_digest_path
    
    # 如果在 PATH 中找不到，尝试在项目目录中查找
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_pt_query_digest = os.path.join(script_dir, 'pt-query-digest')
    if os.path.isfile(project_pt_query_digest):
        return project_pt_query_digest
    
    # 如果都找不到，返回 None
    return None

@app.route('/')
@app.route('/<path:filename>')
def serve_files(filename='index.html'):
    full_path = os.path.join(SERVE_DIRECTORY, filename)
    
    if os.path.isfile(full_path):
        # 如果是文件，直接发送
        return send_from_directory(SERVE_DIRECTORY, filename)
    elif os.path.isdir(full_path):
        # 如果是目录，显示目录内容
        files = os.listdir(full_path)
        return render_template('directory.html', files=files, current_path=filename)
    else:
        # 如果路径不存在，返回 404
        abort(404)

@app.route('/v1')
def index_v1():
    return send_file('index-v1.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'log_file' not in request.files:
        print(request.files)
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['log_file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        filename = file.filename
        file.save(filename)
        
        try:
            pt_query_digest_path = get_pt_query_digest_path()
            if not pt_query_digest_path:
                raise FileNotFoundError("无法找到 pt-query-digest")

            result = subprocess.run([pt_query_digest_path, '--limit', '100%', '--output=json', filename], 
                                    capture_output=True, 
                                    text=True, 
                                    check=True)
            
            # 解析 JSON 输出
            analysis = json.loads(result.stdout)
            
            
            return jsonify(analysis)
        except FileNotFoundError as e:
            return jsonify({'error': f'找不到 pt-query-digest: {str(e)}'}), 500
        except subprocess.CalledProcessError as e:
            # 如果命令执行失败，e.output 将包含标准输出，e.stderr 将包含标准错误
            print("命令执行失败")
            print("返回码:", e.returncode)
            print("标准输出:", e.output)
            print("标准错误:", e.stderr)
            return jsonify({'error': f'pt-query-digest 执行失败: {e}'}), 500
        except json.JSONDecodeError as e:
            return jsonify({'error': f'JSON 解析失败: {e}'}), 500
        except Exception as e:
            # 捕获其他可能的异常
            print("发生异常:", str(e))
            return jsonify({'error': f'发生未知错误: {str(e)}'}), 500
        finally:
            # 删除临时文件
            os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True)
